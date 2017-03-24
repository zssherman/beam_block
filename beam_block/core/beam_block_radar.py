# Note docstring below is as if beam_block will be added
# to Py-ART in the future.

# This code is based on code and help from Kai Muehlbauer,
# Nick Guy and Scott Collis.

"""
pyart.retrieve.beam_block_radar
=======================================

Calculates partial beam block(PBB) and cumulative beam block(CBB)
by using wradlib's beamblock and geotiff functions. PBB and CBB
are then used to created flags when a certain beam block fraction
is passed.

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
    proj_raster = wrl.georef.wkt_to_osr(data_raster.GetProjection())
    rastercoords, rastervalues = wrl.io.read_raster_data(rasterfile)
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
        index_end = radar.sweep_end_ray_index['data'][i]

        elevs = radar.elevation['data'][index_start:index_end + 1]
        azimuths = radar.azimuth['data'][index_start:index_end + 1]
        rg, azg = np.meshgrid(_range, azimuths)
        rg, eleg = np.meshgrid(_range, elevs)
        lon, lat, alt = wrl.georef.polar2lonlatalt_n(
            rg, azg, eleg, sitecoords)

        x_pol, y_pol = wrl.georef.reproject(
            lon, lat, projection_target=proj_raster)
        polcoords = np.dstack((x_pol, y_pol))
        rlimits = (x_pol.min(), y_pol.min(), x_pol.max(), y_pol.max())
        ind = wrl.util.find_bbox_indices(rastercoords, rlimits)
        rastercoords = rastercoords[ind[1]:ind[3], ind[0]:ind[2], ...]
        rastervalues = rastervalues[ind[1]:ind[3], ind[0]:ind[2]]

        # Map rastervalues to polar grid points
        polarvalues = wrl.ipol.cart2irregular_spline(
            rastercoords, rastervalues, polcoords)

        pbb = wrl.qual.beam_block_frac(polarvalues, alt, beamradius)
        pbb = np.ma.masked_invalid(pbb)
        pbb_arrays.append(pbb)

        maxindex = np.nanargmax(pbb, axis=1)
        cbb = np.copy(pbb)
        # Iterate over all beams
        for ii, index in enumerate(maxindex):
            premax = 0.
            for jj in range(index):
                # Only iterate to max index to make this faster
                if pbb[ii, jj] > premax:
                    cbb[ii, jj] = pbb[ii, jj]
                    premax = cbb[ii, jj]
                else:
                    cbb[ii, jj] = premax
            # beyond max index, everything is max anyway
            cbb[ii, index:] = pbb[ii, index]
        cbb_arrays.append(cbb)

    pbb_all = np.ma.concatenate(pbb_arrays)
    cbb_all = np.ma.concatenate(cbb_arrays)
    return pbb_all, cbb_all

def beam_block_flags(pbb_all, cbb_all, pbb_threshold,
                     cbb_threshold):
    """ Takes PBB and CBB arrays created from the
    beam_block function and user chosen thresholds
    to create and array of 1s and 0s, 1 is a flagged gate
    where the fraction value is past the threshold. """
    pbb_flags = np.empty_like(pbb_all)
    pbb_flags[pbb_all > pbb_threshold] = 1
    pbb_flags[pbb_all < pbb_threshold] = 0

    cbb_flags = np.empty_like(cbb_all)
    cbb_flags[cbb_all > cbb_threshold] = 1
    cbb_flags[cbb_all < cbb_threshold] = 0
    return pbb_flags, cbb_flags
