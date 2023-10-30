import sys
import argparse
import json
import datetime

import pystac
from pystac.utils import str_to_datetime

import rasterio 

from rio_stac.stac import PROJECTION_EXT_VERSION, RASTER_EXT_VERSION, EO_EXT_VERSION
from rio_stac.stac import (
    get_dataset_geom, 
    get_projection_info,
    get_raster_info,
    get_eobands_info,
    bbox_to_geom,
)

import xstac

def stac_tiff():
    return None 

def stac_xarray():
    return None 
