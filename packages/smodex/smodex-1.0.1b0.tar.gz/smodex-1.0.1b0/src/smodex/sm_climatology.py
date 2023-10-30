""" Soil Moisture Indices Package: Core Module to implement the computation
of soil moisture indices from climate datasets"""

import argparse
import logging

# import necessary packages
import os
import sys
from datetime import datetime
from pathlib import Path

import xarray as xr


# define logging format
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]:%(name)s:%(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class SMClimatology:
    """Computes Soil Moisture Climatology"""

    def __init__(
        self,
        in_path: str,
        climatology_path: str,
        reference: tuple = ("1991-01-01", "2020-12-31"),
    ) -> None:
        self.in_path = in_path  # input path; same as sm_download_path
        self.climatology_path = climatology_path
        self.reference = reference

    def get_archive(self):
        """stacks up all the downloaded soil moisture datasets; expects a NetCDF file
        containing the daily soil moisture content provided at different depths.
        Args:
            in_path (str): directory to raw ERA5 soil moisture datasets

        Returns:
            era_stack(xArray Datasets): stacked up ERA5 soil moisture datasets
        """

        logger.info(f"loading available soil moisture files in input folder {self.in_path}")
        sm_files = []
        for path in Path(self.in_path).rglob("*.nc"):
            sm_files.append(path)

        era_stack = xr.open_mfdataset(
            sm_files,
            concat_dim="time",
            combine="nested",
            data_vars="minimal",
            coords="minimal",
            compat="override",
            parallel=True,
        )
        logger.info("Soil Moisture Stack created")

        era_stack = era_stack.rename({"longitude": "lon", "latitude": "lat"})
        era_stack = era_stack.sortby("time")
        era_stack = era_stack.where((era_stack >= 0) & (era_stack <= 1))
        return era_stack

    def get_climatology_stack(self, era_stack, monthly=False, dekad=False):
        """Stack up soil moisture either dekadly or monthly

        Args:
            stack (xArray Dataset): soil moisture stack
            monthly (bool, optional): Defaults to False.
            dekad (bool, optional): Defaults to False.
        Returns:
            (clim_avg, clim_std): xarray climatological stack
        """

        if monthly:
            era_stack = era_stack.rolling(time=30).mean()
        if dekad:
            era_stack = era_stack.rolling(time=10).mean()
        clim_avg = era_stack.groupby("time.dayofyear").mean("time", skipna=True)
        clim_std = era_stack.groupby("time.dayofyear").std("time", skipna=True)
        return clim_avg, clim_std

    def compute_climatology(self):
        """Compute soil moisture climatology

        Args:
            in_path (str): directory to the raw annual soil moisture files
            out_path (str): directory to save newly generated climatological files
        """
        if not os.path.exists(self.climatology_path):
            os.makedirs(self.climatology_path)

        start = datetime.strptime(self.reference[0], "%Y-%m-%d").year
        end = datetime.strptime(self.reference[1], "%Y-%m-%d").year

        clim_avg_file = Path(self.climatology_path, f"/ERA5_clim_avg_{start}_{end}.nc")
        clim_std_file = Path(self.climatology_path, f"/ERA5_clim_std_{start}_{end}.nc")

        if not clim_std_file.is_file() or not clim_avg_file.is_file():
            era5 = self.get_archive()
            era5 = era5.sel(time=slice(self.reference[0], self.reference[1]))
            # compute climatology
            clim_avg, clim_std = self.get_climatology_stack(era5, dekad=True)
            if not clim_avg_file.is_file():
                clim_avg.to_netcdf(self.climatology_path + f"/ERA5_clim_avg_{start}_{end}.nc")
            if not clim_std_file.is_file():
                clim_std.to_netcdf(self.climatology_path + f"/ERA5_clim_std_{start}_{end}.nc")
            clim_avg.close()
            clim_std.close()


if __name__ == "__main__":
    # command line option
    parser = argparse.ArgumentParser(description="computes the soil moisture climatology")
    parser.add_argument("in_path", type=str, help="path to the downloaded soil moisture")
    parser.add_argument("climatology_path", type=str, help="path to save computed climatology")
    parser.add_argument(
        "-r",
        "--reference",
        nargs="+",
        required=True,
        help="reference dates to compute climatology for",
    )

    args = parser.parse_args()

    sm_climate = SMClimatology(args.in_path, args.climatology_path, args.reference)
    sm_climate.compute_climatology()
