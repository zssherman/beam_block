"""
beam_block.core.beam_block_json
===============================

Calculates partial beam block(PBB) and cumulative beam block(CBB)
by using wradlib's beamblock and geotiff functions. PBB and CBB
are then used to created flags when a certain beam block fraction
is passed.

This code is adapted from code written by Kai Muehlbauer:

https://github.com/wradlib/wradlib/blob/master/notebooks/beamblockage/
wradlib_beamblock.ipynb

Note: The json format is based on X-SAPR variable format. Other radar formats
may be added in the future.

.. autosummary::
    :toctreeL generated/
    :template: dev_template.rst

    json_beam_block

"""

import json
import numpy as np
import wradlib as wrl


def json_beam_block(json_data, tif_file,
                    beam_width=1.0):
    """
    Beam Block Json Calculation

    Parameters
    ----------
    json_data : Json
        Json object used.
    tif_name : string
        Name of geotiff file to use for the
        calculation

    Other Parameters
    ----------------
    beam_width : float
        Radar's beam width for calculation.
        Default value is 1.0.

    Returns
    -------
    pbb_all : array
        Array of partial beam block fractions for each
        gate in all sweeps.
    cbb_all : array
        Array of cumulative beam block fractions for
        each gate in all sweeps.

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

    Helmus, J.J. & Collis, S.M., (2016). The Python ARM
    Radar Toolkit (Py-ART), a Library for Working with
    Weather Radar Data in the Python Programming Language.
    Journal of Open Research Software. 4(1), p.e25.
    DOI: http://doi.org/10.5334/jors.119

    """

    variables = json_data['variables']

    # Opening the tif file and getting the values ready to be
    # converted into polar values.
    rasterfile = tif_file
    data_raster = wrl.io.open_raster(rasterfile)
    rastervalues, rastercoords, proj = wrl.georef.extract_raster_dataset(
        data_raster, nodata=None)
    sitecoords = (np.float(variables['longitude']['data']),
                  np.float(variables['latitude']['data']),
                  np.float(variables['altitude']['data']))

    pbb_arrays = []
    cbb_arrays = []
    _range = np.array(json.loads(variables['range']['data']))
    # Cycling through all sweeps in the radar object.
    beamradius = wrl.util.half_power_radius(_range, beam_width)
    for i in range(
            len(np.array(
                json.loads(variables['sweep_start_ray_index']['data'])))):
        index_start = np.array(
            json.loads(variables['sweep_start_ray_index']['data']))[i]
        index_end = np.array(
            json.loads(variables['sweep_end_ray_index']['data']))[i] + 1

        elevs = np.array(
            json.loads(
                variables['elevation']['data']))[index_start:index_end]
        azimuths = np.array(
            json.loads(
                variables['azimuth']['data']))[index_start:index_end]
        rg, azg = np.meshgrid(_range, azimuths)
        rg, eleg = np.meshgrid(_range, elevs)
        lon, lat, alt = wrl.georef.polar2lonlatalt_n(
            rg, azg, eleg, sitecoords)

        x_pol, y_pol = wrl.georef.reproject(
            lon, lat, projection_target=proj)
        polcoords = np.dstack((x_pol, y_pol))
        rlimits = (x_pol.min(), y_pol.min(), x_pol.max(), y_pol.max())
        ind = wrl.util.find_bbox_indices(rastercoords, rlimits)
        rastercoords = rastercoords[0:ind[3], ind[0]:ind[2], ...]
        rastervalues = rastervalues[0:ind[3], ind[0]:ind[2]]

        # Map rastervalues to polar grid points.
        polarvalues = wrl.ipol.cart2irregular_spline(
            rastercoords, rastervalues, polcoords)

        # Calculate partial beam blockage using wradlib.
        pbb = wrl.qual.beam_block_frac(polarvalues, alt, beamradius)
        pbb = np.ma.masked_invalid(pbb)
        pbb_arrays.append(pbb)

        # Calculate cumulative beam blockage using wradlib.
        cbb = wrl.qual.cum_beam_block_frac(pbb)
        cbb_arrays.append(cbb)

    # Stacks all sweeps blockage data.
    pbb_all = np.ma.concatenate(pbb_arrays)
    cbb_all = np.ma.concatenate(cbb_arrays)
    return pbb_all, cbb_all
