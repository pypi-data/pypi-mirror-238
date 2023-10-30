"""
    Soil Moisture Downloader: Configured to download datasets from the Climate Data Store
    Downloads hourly soil moisture datasets for full year
"""

import argparse
import json
import logging
import os
import sys

import numpy as np
import pandas as pd

import cdsapi


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


api_client = cdsapi.Client()


def cds_downloader(start_date: str, end_date: str, conf_path: str, download_path: str) -> None:
    """Downloads specified variables (e.g. volumetric soil water content) detailed in a
    config file from ERA5 Climate Data Store for a specified time range (start and end date)

    Args:
        start_date (str): initial date to start downloading datasets from e.g. '2001-01-01'
        end_date (str): last date to stop downloading datasets for e.g. '2045-12-31'
        conf_path (str): directory to CDS API configuration json file e.g. \
            configs/download_conf.json
        download_path (str): directory to save the downloaded datasets in e.g. era_sm/
    """

    with open(conf_path) as file:
        conf = json.load(file)

    date_ranges = pd.date_range(start=start_date, end=end_date)
    year_ranges = np.unique([date.year for date in date_ranges])

    for yr in year_ranges:
        conf["year"] = int(yr)
        logger.info(f"downloading ERA5 Soil Moisture from CDS API for {yr}")
        if not os.path.exists(download_path):
            os.makedirs(download_path)
        api_client.retrieve(
            "reanalysis-era5-single-levels", conf, download_path + f"ERA5_SM_{yr}.nc"
        )
        logger.info(f"Downloaded soil moisture now available at {download_path+f'ERA5_SM_{yr}.nc'}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Downloads soil moisture datasets from start date \
            to end date from ERA5 Climate Data Store"
    )

    parser.add_argument(
        "start_date",
        type=str,
        help="initial date to start \
                                     downloading from e.g. 2001-01-01",
    )

    parser.add_argument(
        "end_date",
        type=str,
        help="end date to stop \
                                     downloading datasets from e.g. 2030-12-31",
    )

    parser.add_argument(
        "conf_path",
        type=str,
        help="directory to download configuration json file e.g. configs/download.json",
    )

    parser.add_argument(
        "download_path",
        type=str,
        help="directory to save the \
                        downloaded datasets e.g. sm_downloaded/",
    )

    args = parser.parse_args()

    cds_downloader(args.start_date, args.end_date, args.conf_path, args.download_path)
