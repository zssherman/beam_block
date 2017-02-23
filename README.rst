Beam Block
==========

Using Wradlib and Py-ART to obtain partial beam block (PBB) and cumulative beam block (CBB) data. The data then can be used to create flags and also can be added as fields to an empty radar object or an existing radar object, if the existing radar object fields have the same shape as the beamblock data and flag fields.

Note: This project is still a work in progress.

Dependencies
------------

- `Py-ART <http://arm-doe.github.io/pyart/>`_
- `Wradlib <http://wradlib.org/wradlib-docs/latest/index.html>`_

Also needs a special environment due to gdal::

        conda create -n gdal_test -c conda-forge python=3.5 basemap gdal

Bash Command
------------

To run beam block in bash::

        python /home/user/bb_from_radar <radar_file> <tif_file> <out_file>

With some work bb_from_radar can be created into a command for simpler use.
If anaconda3 is installed, you can run the bb_from_radar file as a command.
To do so, first::

        mv /home/user/bb_from_radar /home/user/anaconda3/bin/bb_from_radar

Then to activate::

        chmod -x /home/user/anaconda3/bin/bb_from_radar

To run beam block is now::

        bb_from_radar <radar_file> <tif_file> <out_file>

If anaconda3 isn't installed, the ~/.bashrc file needs to be edited to contain
a file path to the bb_from_radar file. Moving bb_from_radar to anaconda3/bin
if it is installed utilizes the already export PATH created by conda. To add a path if anaconda3 isn't installed::

        vim ~./bashrc

At the end of the file add::

        export PATH/home/user/filelocation:$PATH

Then to activate::

        chmod -x /home/user/filelocation/bb_from_radar

To run beam block is now::

         bb_from_radar <radar_file> <tif_file> <out_file>

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
