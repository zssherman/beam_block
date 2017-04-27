"""
beam_block.core.beam_block_radar
================================

Calculates partial beam block(PBB) and cumulative beam block(CBB)
by using wradlib's beamblock and geotiff functions. PBB and CBB
are then used to created flags when a certain beam block fraction
is passed.

This code is adapted from code written by Kai Muehlbauer:

https://github.com/wradlib/wradlib/blob/master/notebooks/beamblockage/
wradlib_beamblock.ipynb

.. autosummary::
    :toctreeL generated/
    :template: dev_template.rst

    beam_block
    beam_block_flags

"""

import numpy as np
import wradlib as wrl


def beam_block(radar, tif_file,
               beam_width=1.0):
    """
    Beam Block Radar Calculation

    Parameters
    ----------
    radar : Radar
        Radar object used.
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
    # Emptying the radar fields.
    radar.fields.clear()

    # Opening the tif file and getting the values ready to be
    # converted into polar values.
    rasterfile = tif_file
    data_raster = wrl.io.open_raster(rasterfile)
    rastervalues, rastercoords, proj = wrl.georef.extract_raster_dataset(
        data_raster, nodata=None)
    sitecoords = (np.float(radar.longitude['data']),
                  np.float(radar.latitude['data']),
                  np.float(radar.altitude['data']))

    pbb_arrays = []
    cbb_arrays = []
    _range = radar.range['data']
    beamradius = wrl.util.half_power_radius(_range, beam_width)
    # Cycling through all sweeps in the radar object.
    for i in range(len(radar.sweep_start_ray_index['data'])):
        index_start = radar.sweep_start_ray_index['data'][i]
        index_end = radar.sweep_end_ray_index['data'][i] + 1

        elevs = radar.elevation['data'][index_start:index_end]
        azimuths = radar.azimuth['data'][index_start:index_end]
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

    pbb_all = np.ma.concatenate(pbb_arrays)
    cbb_all = np.ma.concatenate(cbb_arrays)
    return pbb_all, cbb_all


def beam_block_flags(pbb_all, cbb_all, no_block_thresh=0.01,
                     complete_block_thresh=0.95):
    """
    Takes PBB and CBB arrays created from the beam_block function
    and creates beam block flags.

    Parameters
    ----------
    pbb_all : array
        Array of partial beam blockage values created from the beam_block
        function.
    cbb_all : array
        Array of cumulative beam blockage values created from the beam_block
        function.

    Other Parameters
    ----------------
    no_block_thresh : float
        Value for the cutoff for no blockage flag value of 0. Anything below
        the no_block_thres is considered not blocked. Default value is 0.01.
    complete_block_thresh : float
        Value for the cutoff for complete blockage flag value of 2. Anything
        above the complete_block_thres is considered blocked. Default value
        is 0.95.

    Returns
    -------
    pbb_flags : array
        Array of integer values depicting no, partial, and complete beam
        blockage based on the partial beam blockage data. This array can then
        be used to create a partial beam block flags field.
    cbb_flags : array
        Array of integer values depicting no, partial, and complete beam
        blockage based on the cumulative beam blockage data. This array can
        then be used to create a cumulative beam block flags field.

    Note
    ----
    The no_block_thresh and complete_block_thresh are also used to created
    the partial blockage flag value of 1, by having anything between the
    no_block_thresh and complete_block_thresh = 1.

    """
    pbb_flags = np.empty_like(pbb_all)
    pbb_flags[pbb_all > complete_block_thresh] = 2
    pbb_flags[
        (pbb_all > no_block_thresh) & (pbb_all < complete_block_thresh)] = 1
    pbb_flags[pbb_all < no_block_thresh] = 0

    cbb_flags = np.empty_like(cbb_all)
    cbb_flags[cbb_all > complete_block_thresh] = 2
    cbb_flags[
        (cbb_all > no_block_thresh) & (cbb_all < complete_block_thresh)] = 1
    cbb_flags[cbb_all < no_block_thresh] = 0
    return pbb_flags, cbb_flags
