""" Contains multiple test cases for the sm_climatology() module"""

import os
import shutil
import subprocess

import numpy as np
import pandas as pd
import xarray as xr

import pytest
from smodex.sm_climatology import SMClimatology


@pytest.fixture
def tmpdir(tmpdir_factory):
    """Create temporary directory for testing"""
    return tmpdir_factory.mktemp("test_dir")


def create_sythentic_dataset(date_range):
    """generates synthetic xArray soil moisture Dataset

    Args:
        date_range (Datetime Index): Date range contains start and end date of sample test dataset

    Returns:
        xArray Dataset: synthetic xarray dataset
    """
    lon = np.linspace(-180, 180, 360)
    lat = np.linspace(-90, 90, 180)

    data = np.random.random((730, 180, 360))
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


def test_invalid_reference(tmpdir):
    """check for valid climatology reference start and end dates

    Args:
        tmpdir (tmpdir): temporary directory for testing
    """

    archive_path = tmpdir.mkdir("archive")
    climatology_path = tmpdir.mkdir("climatology")

    reference = ("invalid_start", "invalid_end")

    with pytest.raises(ValueError):
        sm_climate = SMClimatology(str(archive_path), str(climatology_path), reference)

        sm_climate.compute_climatology()

    # Cleanup
    shutil.rmtree(tmpdir)


# @pytest.mark.skip(reason="skip while performing tests with the others")
def test_compute_climatology(tmpdir):
    """Test  the SM Climatology produces the correct file output.

    Args:
        tmpdir (tmpdir): temporary directory for testing
    """

    date_range = pd.date_range(start="2005-01-01", end="2006-12-31", freq="D")
    syn_ds = create_sythentic_dataset(date_range)

    archive_path = tmpdir.mkdir("archive")
    climatology_path = tmpdir.mkdir("climatology")

    # generate multi-year soil moisture data
    for dat in np.unique(date_range.year):
        syn_ds.sel(time=slice(str(dat) + "-01-01", str(dat) + "-12-31")).to_netcdf(
            f"{archive_path}/soil_moisture_{str(dat)}.nc"
        )
    syn_ds.close()

    # Test case parameters
    reference = (date_range[0].strftime("%Y-%m-%d"), date_range[-1].strftime("%Y-%m-%d"))

    # Run the SMClimatology class
    sm_climate = SMClimatology(str(archive_path), str(climatology_path), reference)
    sm_climate.compute_climatology()

    # Check if climatology files were generated
    clim_avg_file = f"{climatology_path}" + "/ERA5_clim_avg_2005_2006.nc"
    clim_std_file = f"{climatology_path}" + "/ERA5_clim_std_2005_2006.nc"

    assert os.path.exists(clim_avg_file)
    assert os.path.exists(clim_std_file)

    # Cleanup
    shutil.rmtree(tmpdir)


# Test get_climatology_stack function
# @pytest.mark.skip(reason="skip while performing tests with the others")
def test_get_climatology_stack():
    """
    Tests the rolling mean of the climatology stack matching dimensions
    """

    # Create a synthetic dataset
    date_range = pd.date_range(start="2005-01-01", end="2006-12-31", freq="D")
    syn_ds = create_sythentic_dataset(date_range)

    # Instantiate SMClimatology
    sm_climate = SMClimatology(
        "", "", reference=(date_range[0].strftime("%Y-%m-%d"), date_range[-1].strftime("%Y-%m-%d"))
    )

    # Test monthly climatology
    clim_avg_monthly, clim_std_monthly = sm_climate.get_climatology_stack(syn_ds, monthly=True)
    assert clim_avg_monthly.dims == clim_std_monthly.dims
    assert clim_avg_monthly.sizes == clim_std_monthly.sizes

    # Test dekadly climatology
    clim_avg_dekadly, clim_std_dekadly = sm_climate.get_climatology_stack(syn_ds, dekad=True)
    assert clim_avg_dekadly.dims == clim_std_dekadly.dims
    assert clim_avg_dekadly.sizes == clim_std_dekadly.sizes

    # Test without rolling
    clim_avg_none, clim_std_none = sm_climate.get_climatology_stack(syn_ds)
    assert clim_avg_none.dims == clim_std_none.dims
    assert clim_avg_none.sizes == clim_std_none.sizes


# test cli output
# @pytest.mark.parametrize("archive_path, climatology_path, reference", [
#     (tmpdir_factory.mktemp("archive"), tmpdir_factory.mktemp("climatology"),
# ["2005-01-01", "2006-12-31"]),
# ])

# def test_cli_execution(archive_path, climatology_path, reference, capsys):
#     # Prepare the command-line arguments
#     cmd = ["python", "smodex/sm_climatology.py", archive_path, climatology_path, "-r"] + reference

#     # Run the script and capture stdout and stderr
#     subprocess.run(cmd, check=True)

#     # Capture the printed output
#     captured = capsys.readouterr()
#     assert "Soil Moisture Stack created" in captured.out
#     assert "Climatology computation complete" in captured.out
<<<<<<< HEAD

if __name__ == "__main__":
    pytest.main()
=======
>>>>>>> e26b415 (rebase merge request)
