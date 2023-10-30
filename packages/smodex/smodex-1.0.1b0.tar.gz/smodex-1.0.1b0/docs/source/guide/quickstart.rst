Getting Started
===============
The goal of the smodex package is to ensure the seamless computation of soil moisture 
anomalies from climate datasets. Hence, the main steps involved in this computation 
have been simplified to:

#. Data Loading, 
#. Climatology computation,
#. Anomalies computation,
#. Data visualization, and
#. Data sharing

In this page, we walk you through how to utilize the main functionalities of the `smodex`_ package to perform
these actions. Ensure you have the smodex package, you can consult the installation guide for the different 
ways of installing the package in your development environment.


1. Data Loading
----------------
The smodex downloader module provides functionalities that enables you access datasets from the  
`ERA5 Climate Data Store`_ by specifying the details of the requested datasets in a JSON file and providing all the neccesary 
information for downloading the datasets you need. To do this, follow the following steps:

#. Step 1. Ensure you have the `ERA5 CDS API` installed in your development environment. This can be done by:

.. code-block:: bash

    pip install cdsapi


This provides all the neccesary functionalities and backends for accessing the CDS datasets. 

Next to this, create a configuration file (JSON file) that contains all the data specification for 
the data you would like to request, example:

.. code-block:: json-object

    {
        "product_type": "reanalysis", 
        "variable": [
            "volumetric_soil_water_layer_1",
            "volumetric_soil_water_layer_2",
            "volumetric_soil_water_layer_3",
            "volumetric_soil_water_layer_4"
            ],
        "year": 1981,
        "month": [ "01", "02", "03"],
        "day": ["01", "08", "16", "24", "30"],
        "time": ["00:00", "06:00", "12:00", "18:00"],
        "area": [47.148, 10.255, 46.297, 12.542],
        "format": "netcdf"
        }



This JSON file in general should contain the information on your **Area of Interest** and other 
specific information on the datasets you would like to download.


#. Step 2. Specify the time range (start date and end date) and download your data to the specified path:

.. code-block:: python

    from smodex.downloader import cds_downloader
    start_date = '2010-01-01'
    end_date = '2020-12-31'
    conf_path = 'download.json'
    download_path = 'moisture_data/'
    
    cds_downloader(start_date = start_date,
                   end_date = end_date,
                   conf_path = conf_path,
                   download_path = download_path
                   )


1. Download data files
2. Compute climatology based on reference period
3. Compute anomaly based on specified time-scale



2. Climatology computation
--------------------------
This steps simply computes the average and standard deviation of soil moisture climatology using one of
a weekly, dekadal, or monthly rolling means. The expected file input is an annual netcdf file that 
contains daily volumetric soil water layers (see the previous step for direction on how to access this 
data from the Climate Data Store)


.. code-block:: python

    from smodex.sm_climatology import SMClimatology
    input_path = "path/to/raw/soil_moisture_files/"
    clim_path = "path/to/to/be/computed/climatological/files/"
    reference_dates = ('1991-01-01', '2020-12-31') # climatology reference period
    
    sm_climate = SMClimatology(in_path,
                               climatology_path,
                               reference)
    sm_climate.compute_climatology()



3. Anomalies computation
------------------------
With the previous steps, we are now ready to compute the soil moisture anomalies for our area of interest using the 
`compute_anomalies()` function. 


.. code-block:: python 

    in_path = "path/to/raw/soil_moisture_files/"
    out_path = "path/to/store/anomalies/files"
    clim_path = "path/to/computed/climatological/files/"
    reference=("1991-01-01", "2020-12-31")
    c_year="2012" # year to compute anomalies for
    out_format="netcdf" # output format
    area=(3.685, 42.991, 17.162, 50.565)
    interp_method="linear"
    espg_code="3035"
    

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
        )



4. Data visualization
------------------------
Coming soon!



5. Data sharing
---------------
Coming soon!



.. _`ERA5 Climate Data Store`: https://cds.climate.copernicus.eu/cdsapp#!/search?type=dataset
.. _`smodex`: https://pypi.org/project/smodex/ 
