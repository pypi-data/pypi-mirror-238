import os
from unittest.mock import Mock
from unittest.mock import patch

import cdsapi
import pytest
from smodex.downloader import cds_downloader


@pytest.fixture
def mock_cdsapi_client():
    # Create a mock object for the cdsapi.Client class
    mock_client = Mock(spec=cdsapi.Client())
    return mock_client


def test_downloader(tmp_path, monkeypatch, caplog):
    # test data
    start_date = "2021-01-01"
    end_date = "2021-12-31"
    conf_path = str("download.json")
    download_path = str(tmp_path)

    # Monkeypatch the os.makedirs function to avoid creating directories during testing
    monkeypatch.setattr(os, "makedirs", lambda path: None)

    cds_downloader(start_date, end_date, conf_path, download_path)

    assert "downloading ERA5 Soil Moisture from CDS API for 2021" in caplog.text
    assert (
        f"Downloaded soil moisture now available at {download_path+f'ERA5_SM_{2021}.nc'}"
        in caplog.text
    )


if __name__ == "__main__":
    pytest.main()
