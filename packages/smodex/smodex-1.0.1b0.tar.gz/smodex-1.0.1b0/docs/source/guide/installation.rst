.. _install: 

Installation
============ 
The smodex package is distributed via the Python Package Index and also available on the 
`development repo`_. To enable 
the full functionalities, install also the `cdsapi`_


Option 1: Use Pip (Recommended)
-------------------------------
The easiest way is to use pip, which contains the latest release of the package. 
Install pip in your development environment, if you do not have pip installed yet, 
if you do not have pip installed yet.


.. code-block:: bash 

    pip install smodex


Option 2: Clone the repository
------------------------------
The latest development version of the smode package is available on the 
`GitLab repo`_. 


.. caution::
    The version on the repo is  not guaranteed to be stable, but in 
    general contains new features that are yet to be released

.. code-block:: bash 

    git clone https://gitlab.inf.unibz.it/earth_observation_public/smodex
    cd smodex
    python setup.py install 


.. _development repo: https://gitlab.inf.unibz.it/earth_observation_public/smodex
.. _GitLab repo: https://gitlab.inf.unibz.it/earth_observation_public/smodex
.. _cdsapi: https://cds.climate.copernicus.eu/api-how-to
