"""
Module for computing soil moisture anomalies
Recommended data input format is NetCDF
"""

import argparse
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr

import pyproj


# define logging format
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]:%(name)s:%(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_matching_files(in_path: str, start_date: str, end_date: str) -> list:
    """extract grib files within the specified date range
    # if user wants to use grib files

    Returns:
        list: a list of volumetric soil moisture files
    """

    date_format = "%Y_%-m_%-d"
    sma_date_range = pd.date_range(start=start_date, end=end_date).strftime(date_format).tolist()

    sm_files = [
        path
        for path in Path(in_path).rglob("volumetric_soil_water_layer*.grib")
        if "_".join(os.path.splitext(path.name)[0].split("_")[-4:-1]) in sma_date_range
    ]
    return sm_files


def get_extent(
    area=(3.685, 42.991, 17.162, 50.565),
    proj="WGS84",
):
    """returns the bounding box for the ADO extent: minlon, minlat, maxlon, maxlat

    Args:
    area (list): order: minlon, minlat, maxlon, maxlat
    proj (str, optional): projection type. Defaults to 'WGS84' or LAEA,
                        Otherwise specify the epsg code https://epsg.io/transform
    """

    minlon = area[0]
    minlat = area[1]
    maxlon = area[2]
    maxlat = area[3]

    if proj == "WGS84":
        return minlon, minlat, maxlon, maxlat
    else:
        try:
            source_proj = pyproj.Proj("epsg:4326")
            target_proj = pyproj.Proj(f"epsg:{proj}")
            minlat, minlon = pyproj.transform(source_proj, target_proj, minlat, minlon)
            maxlat, maxlon = pyproj.transform(source_proj, target_proj, maxlat, maxlon)
            return minlon, minlat, maxlon, maxlat
        except pyproj.exceptions.CRSError as e:
            print(f"EPSG:{proj} does not exist or is not supported: {e}")
    return None


def resample_interpolate_grid(grid, area, interp_method="linear", espg_code="3035"):
    """interpolate ERA 5 to match to the defined grid and resolution using ]
    bilinear interpolation and set projection

    Args:
        grid (xarray dataset): input file to resample
        interp_method: interpolation methods -- options {"linear",
        "nearest", "zero", "slinear", "quadratic", "cubic", "polynomial"}

    Returns:
        grid_laea (xarray dataset): resampled file
    """

    grid.rio.set_spatial_dims("lon", "lat")
    grid.rio.write_crs("EPSG:4326", inplace=True)
    grid_proj = grid.rio.reproject(f"EPSG:{espg_code}")

    aoi_extent = get_extent(area=area,
                            proj=espg_code)

    # extract target grid
    x_target = np.arange(aoi_extent[0], aoi_extent[2], 5000) + 2500
    y_target = np.arange(aoi_extent[3], aoi_extent[1], -5000) + 2500

    grid_proj = grid_proj.interp(x=x_target, y=y_target, method=interp_method)
    return grid_proj


def compute_anomalies(
    in_path,
    out_path,
    clim_path,
    reference=("1991-01-01", "2020-12-31"),
    c_year="2019",
    out_format="netcdf",
    area=(3.685, 42.991, 17.162, 50.565),
    interp_method="linear",
    espg_code="3035"
):
    """computes soil moisture anomalies
    Args:
        in_path (str): directory to the daily volumetric soil moisture
        out_path (str): directgory to save newly computed soil moisture anomalies
        clim_path (str): directory to static soil moisture climatology computed
    """
    # TODO: include a scale that allows computation for short date range, monthly, and annual

    if not os.path.exists(out_path):  # create output path
        os.makedirs(out_path)

    # load climatology
    start_year = datetime.strptime(reference[0], "%Y-%m-%d").year
    end_year = datetime.strptime(reference[1], "%Y-%m-%d").year

    clim_avg = xr.open_dataset(
        clim_path + f"/ERA5_clim_avg_{start_year}_{end_year}.nc", decode_cf=True
    ).astype(np.float64)

    clim_std = xr.open_dataset(
        clim_path + f"/ERA5_clim_std_{start_year}_{end_year}.nc", decode_cf=True
    ).astype(np.float64)

    sm_year = xr.open_dataset(in_path + f"/ERA5_SM_{c_year}.nc", decode_cf=True).astype(np.float64)
    sm_year = sm_year.resample(time="1D").mean().dropna("time")
    sm_year = sm_year.rename({"longitude": "lon", "latitude": "lat"})

    for itime in sm_year.time.values:
        itime_dt = pd.to_datetime(itime)
        outfile_name = "era5_sm_anom_" + itime_dt.strftime("%Y%m%d") + ".tif"
        outfile_path = Path(out_path, outfile_name)
        if not outfile_path.is_file():
            logger.info("creating soil moisture anomalies for: " + str(itime))
            sm_day = sm_year.loc[{"time": itime}]
            anom_day = (sm_day - clim_avg.loc[{"dayofyear": itime_dt.dayofyear}]) / clim_std.loc[
                {"dayofyear": itime_dt.dayofyear}
            ]
            res_grid = resample_interpolate_grid(anom_day, area=area,
                                                 interp_method=interp_method,
                                                 espg_code=espg_code)
            if out_format == "netcdf":
                outfile_name = outfile_name[:-4] +".nc"
                outfile_path = Path(out_path, outfile_name)
                res_grid.to_netcdf(outfile_path)
            else:
                res_grid.rio.to_raster(outfile_path)
        else:
            logger.info("already existing:" + str(itime))
    sm_year.close()


if __name__ == "__main__":
    # command line option
    parser = argparse.ArgumentParser(
        description="Soil Moisture Anomaly Computation based on \
                                      specified reference date"
    )
    parser.add_argument(
        "in_path",
        type=str,
        help="input path containing downloaded soil moisture file, expected to be in \
            NetCDF format e.g. '/mnt/CEPH_PROJECTS/ADO/SM/SM_nc/sm_downloaded/'",
    )
    parser.add_argument(
        "out_path",
        type=str,
        help="Output path to store the computed soil moisture anomalies files in the \
            specified format",
    )
    parser.add_argument(
        "clim_path", type=str, help="path to static climatological file, computed earlier"
    )
    parser.add_argument(
        "-r",
        "reference",
        nargs="+",
        required=True,
        help="tuple of the start and end date of the reference time for computing \
            the climatology e.g. ('1991-01-01', '2020-12-31')",
    )
    parser.add_argument(
        "c_year", type=str, help="year to compute soil moisture anomalies for e.g. '2022'"
    )
    parser.add_argument(
        "out_format",
        type=str,
        help="output format to store the computed soil moisture anomalies in e.g. netcdf or tiff",
    )

    args = parser.parse_args()

    compute_anomalies(
        args.in_path, args.out_path, args.clim_path, args.reference, args.c_year, args.out_format
    )
