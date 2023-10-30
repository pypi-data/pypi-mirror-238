.. smodex documentation master file, created by
   sphinx-quickstart on Fri Oct  6 15:31:00 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to the smodex's documentation!
======================================
.. toctree::
   :maxdepth: 2
   :caption: Contents: 

smodex
======

Soil moisture and soil moisture anomalies are critical markers of dryness 
and agricultural drought and is used by researchers, water resource managers and 
policy markers to understand dryness and wetness conditions including dry spells 
and the onset and offset drought in an area. 

**smodex** is a tool that enhances the 
performant computation, visualization and sharing of soil moisture and soil moisture
anomalies using climate datasets. It embraces the principles of FAIR and Open Science 
in the development of the computational workflow and the data sharing for quick and 
easy access within the scientific community.


Features
--------

- Downloads climate datasets from Climate Data Store, 
- Computation of climatological statistics at different rolling means and time-scale, 
- Computes anomalies at different time-scales, 
- Supports Python versions 3.7+
- Released under the `MIT No Attribution license`_.


User guide
-----------

A step by step guide on getting started with smodex package

.. toctree::
   :maxdepth: 2

   guide/installation.rst
   guide/quickstart.rst
   guide/modules.rst
   guide/contributing.rst
  

.. note::
   The smodex package is currently under development and the API documentation is 
   being updated


   
smodex license
--------------
the smodex package is release under the MIT No-Attribution license. 

.. _MIT No Attribution license: https://gitlab.inf.unibz.it/earth_observation_public/smodex/-/blob/master/LICENSE?ref_type=heads
