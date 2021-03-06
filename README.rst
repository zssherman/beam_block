Beam Block
==========

Using Wradlib and Py-ART to obtain partial beam block (PBB) and cumulative
beam block (CBB) data. The data then can be used to create flags and also
can be added as fields to an empty radar object. There is also a function
that calculates the lowest elevation angle needed at each gate to achieve less
than 0.01 cumulative beam blockage.

Note: This project is still a work in progress.

Dependencies
------------

- `Py-ART <http://arm-doe.github.io/pyart/>`_
- `Wradlib <http://wradlib.org/wradlib-docs/latest/index.html>`_

Beam block also needs a special environment due to gdal. Recommended would
be to download `Anaconda <http://continuum.io/downloads>`_ and 
`Miniconda <http://continuum.io/downloads>`_. Then by using `conda` from
Miniconda to create the needed environment, use the following command
in bash::

        conda create -n beam_block_env -c conda-forge python=3.5 basemap gdal

Install
-------

To install Beam Block, after cloning the repository::

        cd beam_block
        python setup.py install

Bash Command
------------

To run beam block in bash, first activate beam_block_env environment::

        source activate beam_block_env

Then to run beam block based on a radar file::

        bb_from_radar <radar_file> <tif_file> <out_file>

To run beam block based on a json file::

        bb_from_json <json_file> <tif_file> <out_file>

There is also an optional beam_width argument, with a default value of 1.0. To
choose a beam_width float value, the terminal command now becomes::

        bb_from_radar -bw <value> <radar_file> <tif_file> <out_file>

There are also two flag arguments no_block_thresh and complete_block_thresh,
when determining the cutoff for no, partial and complete blockage for the flag
values of 0, 1, 2. To change the default values of 0.01 (no_block_thresh) and
0.95 (complete_block_thresh), the command is::

        bb_from_radar <radar_file> <tif_file> <out_file> -nb <value> -cb <value>

GeoTIFF Data
------------

To obtain GeoTIFF data to be used in the beam blockage calculation,
USGS (U.S. Geological Survey) `EarthExplorer <https://earthexplorer.usgs.gov/>`_
can be used. Under Data Sets choose Digital Elevation and then SRTM (Shuttle
Radar Topography Mission) and check the box for which SRTM data you would liked
to be searched. Data that is search is within your search criteria.

Testing
-------

For unit tests in Beam Block, nosetests from the package `nose <http://nose.readthedocs.io/en/latest/>`_ is used.
In order for nosetests to work with Beam Block, nose needs to be installed in
the gdal_test environment. To do this in bash::

        source activate beam_block_env
        pip install nose -I

To then run the unit tests in Beam Block::

        nosetests beam_block

From inside the directory::

        cd beam_block
        nosetests

If you would like to run nosetests only on a specific test file, for example
test_beam_block_radar.py in the tests folder in the core subpackage, simply
type::

        nosetests '/home/user/beam_block/beam_block/core/tests/test_beam_block_radar.py'

Special Thanks
--------------

Special thanks to Kai Muehlbauer, Nick Guy, Scott Collis, and Jonathan Helmus
for code help and advice!

References
----------

Bech, J., B. Codina, J. Lorente, and D. Bebbington,
2003: The sensitivity of single polarization weather
radar beam blockage correction to variability in the
vertical refractivity gradient. J. Atmos. Oceanic
Technol., 20, 845–855

Heistermann, M., Jacobi, S., and Pfaff, T., 2013:
Technical Note: An open source library for processing
weather radar data (wradlib), Hydrol. Earth Syst.
Sci., 17, 863-871, doi:10.5194/hess-17-863-2013

Helmus, J.J. & Collis, S.M., (2016). The Python ARM Radar Toolkit
(Py-ART), a Library for Working with Weather Radar Data in the
Python Programming Language. Journal of Open Research Software.
4(1), p.e25. DOI: http://doi.org/10.5334/jors.119
