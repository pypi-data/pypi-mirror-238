import os
import shutil
import tempfile
import unittest.mock as mock
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr

import pytest
import rioxarray as rio
from smodex.sm_anomaly import compute_anomalies
from smodex.sm_anomaly import get_extent
from smodex.sm_anomaly import get_matching_files
from smodex.sm_anomaly import resample_interpolate_grid


# Define a temporary directory for testing
@pytest.fixture(scope="module")
def temp_test_dir():
    test_dir = tempfile.mkdtemp()
    yield test_dir
    shutil.rmtree(test_dir)


def generate_day_of_year(start_year, end_year):
    day_of_year = []
    for year in range(start_year, end_year + 1):
        date_range = pd.date_range(start=f"{year}-01-01", end=f"{year}-12-31")
        day_of_year.extend(date_range.dayofyear)

    return day_of_year


def create_synthetic_dataset(start_date, end_date, c_year, clim=False):
    """Generate synthetic xArray soil moisture Dataset.

    Args:
        start_date (str): Start date in "YYYY-MM-DD" format.
        end_date (str): End date in "YYYY-MM-DD" format.
        c_year (str): Year for climatology or target year in "YYYY" format.
        clim (bool): Whether to generate climatology data (True) or daily data (False).

    Returns:
        xr.Dataset: Synthetic xarray dataset.
    """
    lon = np.linspace(-180, 180, 360)
    lat = np.linspace(-90, 90, 180)

    if clim:
        date_range = pd.date_range(start=f"{c_year}-02-15", end=f"{c_year}-03-15", freq="D")
        data = np.random.random((len(date_range), len(lat), len(lon)))
        syn_data = xr.Dataset(
            {
                "swvl1": (["time", "latitude", "longitude"], data),
                "swvl2": (["time", "latitude", "longitude"], data),
                "swvl3": (["time", "latitude", "longitude"], data),
                "swvl4": (["time", "latitude", "longitude"], data),
            },
            coords={"dayofyear": date_range.dayofyear, "latitude": lat, "longitude": lon},
        )
    else:
        date_range = pd.date_range(start=start_date, end=end_date, freq="D")
        data = np.random.random((len(date_range), len(lat), len(lon)))
        syn_data = xr.Dataset(
            {
                "swvl1": (["time", "latitude", "longitude"], data),
                "swvl2": (["time", "latitude", "longitude"], data),
                "swvl3": (["time", "latitude", "longitude"], data),
                "swvl4": (["time", "latitude", "longitude"], data),
            },
            coords={"time": date_range, "latitude": lat, "longitude": lon},
        )

    return syn_data


def test_get_extent():
    extent = get_extent(area=(3.685, 42.991, 17.162, 50.565), proj="WGS84")
    assert extent == (3.685, 42.991, 17.162, 50.565)


def test_resample_interpolate_grid():
    # Create a dummy xarray dataset
    lon = np.arange(3.685, 17.162, 0.1)
    lat = np.arange(50.565, 42.991, -0.1)
    grid = (
        xr.DataArray(
            np.zeros((len(lat), len(lon))), coords={"lon": lon, "lat": lat}, dims=("lat", "lon")
        )
        .astype("int32")
        .rio.write_nodata(-1)
    )

    interpolated_grid = resample_interpolate_grid(grid)
    assert interpolated_grid.dims == ("y", "x")


@pytest.mark.skip(reason="synthetic dataset and anomalies generation takes up too much memory")
def test_compute_anomalies(temp_test_dir):
    # Create dummy input and climatology files
    input_dir = temp_test_dir
    out_path = temp_test_dir
    climatology_dir = temp_test_dir

    start_date = "2005-01-01"
    end_date = "2005-03-31"
    c_year = "2005"
    out_format = "tif"

    # clim_date_range = pd.date_range(start=start_date, end=end_date, c_year=c_year, freq="D")
    # year_date_range = pd.date_range(start="2007-01-01", end="2007-12-31", c_year=c_year, freq="D")

    year_syn = create_synthetic_dataset(start_date, end_date, c_year)
    clim_syn_avg = create_synthetic_dataset(start_date, end_date, c_year, clim=True)
    clim_syn_std = create_synthetic_dataset(start_date, end_date, c_year, clim=True)

    # Create a dummy NetCDF files
    dummy_nc_file_avg = os.path.join(climatology_dir, "ERA5_clim_avg_2005_2005.nc")
    dummy_nc_file_std = os.path.join(climatology_dir, "ERA5_clim_std_2005_2005.nc")
    dummy_year_file = os.path.join(input_dir, f"ERA5_SM_{c_year}.nc")

    year_syn.to_netcdf(dummy_year_file)
    clim_syn_avg.to_netcdf(dummy_nc_file_avg)
    clim_syn_std.to_netcdf(dummy_nc_file_std)

    # Call the compute_anomalies function
    compute_anomalies(
        input_dir, out_path, climatology_dir, (start_date, end_date), c_year, out_format
    )

    # Check if output files were created
    output_files = list(Path(out_path).rglob("era5_sm_anom_*.tif"))
    assert len(output_files) > 0

    # Check if the output files are valid NetCDF files
    for output_file in output_files:
        ds = xr.open_dataset(output_file)
        assert ds is not None


if __name__ == "__main__":
    pytest.main()
