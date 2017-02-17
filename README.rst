Beam Block
==========

Using wradlib and pyart to obtain partial beam block (PBB) and cumulative beam block (CBB) data. The data then can be used to create flags and also can be added as fields to an empty radar object or an existing radar object, if the existing radar object fields have the same shape as the beamblock data and flag fields.

Note: This project is still a work in progress.

Dependencies
------------

- `Py-ART <http://arm-doe.github.io/pyart/>`_
- `Wradlib <http://wradlib.org/wradlib-docs/latest/index.html>`_

Also needs a special environment due to gdal::

        conda create -n gdal_test -c conda-forge python=3.5 basemap gdal

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
