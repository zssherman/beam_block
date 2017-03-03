"""
pyart.retrieve.beam_block_jsom
=======================================

Calculates partial beam block(PBB) and cumulative beam block(CBB)
by using wradlib's beamblock and geotiff functions. PBB and CBB
are then used to created flags when a certain beam block fraction
is passed. Empty radar object is created using Py-ART and then
is filled with beam block data.

.. autosummary::
    :toctreeL generated/
    :template: dev_template.rst

    beam_block_json
    beam_block_flag

"""

import json
import numpy as np
import wradlib as wrl


def beam_block_json(json_file, tif_file,
                    beam_width=1.0):
    """
    Beam Block Calculation

    Parameters
    ----------
    json_file : string
        Name of json file containing radar data.
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
    pbb : array
        Array of partial beam block fractions for each
        gate in each ray.
    cbb: array
        Array of cumulative beam block fractions for
        each gate in each ray.

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

    with open(json_file) as data:
        json_data = json.load(data)

    rasterfile = tif_file
    data_raster = wrl.io.open_raster(rasterfile)
    proj_raster = wrl.georef.wkt_to_osr(data_raster.GetProjection())
    rastercoords, rastervalues = wrl.io.read_raster_data(rasterfile)
    sitecoords = (np.float(json_data['longitude']['data']),
                  np.float(json_data['latitude']['data']),
                  np.float(json_data['altitude']['data']))

    pbb_arrays = []
    cbb_arrays = []
    _range = np.array(json.loads(json_data['range']['data']))
    beamradius = wrl.util.half_power_radius(_range, beam_width)
    for i in range(
            len(np.array(json.loads(json_data['sweep_start_ray_index']['data'])))):
        index_start = np.array(
            json.loads(json_data['sweep_start_ray_index']['data']))[i]
        index_end = np.array(
            json.loads(json_data['sweep_end_ray_index']['data']))[i]

        elevs = np.array(
            json.loads(
                json_data['elevation']['data']))[index_start:index_end + 1]
        azimuths = np.array(
            json.loads(
                json_data['azimuth']['data']))[index_start:index_end + 1]
        rg, azg = np.meshgrid(_range, azimuths)
        rg, eleg = np.meshgrid(_range, elevs)
        lon, lat, alt = wrl.georef.polar2lonlatalt_n(
            rg, azg, eleg, sitecoords)

        x_pol, y_pol = wrl.georef.reproject(
            lon, lat, projection_target=proj_raster)
        polcoords = np.dstack((x_pol, y_pol))
        rlimits = (x_pol.min(), y_pol.min(), x_pol.max(), y_pol.max())
        # Clip the region inside our bounding box
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

def _beam_block_flag(pbb_all, cbb_all, pbb_threshold,
                     cbb_threshold):
    """ Takes PBB and CBB arrays created from the
    beam_block function and user chosen thresholds
    to create and array of 1s and 0s, 1 is a flagged gate
    where the fraction value is past the threshold. """
    pbb_flags = np.empty_like(pbb_all)
    pbb_flags[pbb_all > 0.95] = 3
    pbb_flags[(pbb_all > 0.05) & (pbb_all < 0.95)] = 2
    pbb_flags[pbb_all < 0.05] = 0

    cbb_flags = np.empty_like(cbb_all)
    cbb_flags[cbb_all > 0.95] = 3
    cbb_flags[(cbb_all > 0.05) & (cbb_all < 0.95)] = 2
    cbb_flags[cbb_all < 0.05] = 0
    return pbb_flags, cbb_flags
