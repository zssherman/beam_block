"""
pyart.retrieve.lowest_elevation_no_blockage
===========================================

Calculates the lowest elevation needed to achieve less than
0.01 CBB fraction at every range gate.

.. autosummary
    :toctreeL generated/
    :template: dev_template.rst

    lowest_elevation_no_blockage

"""

import numpy as np
import pyart

from ..core import beam_block


def lowest_elevation_no_blockage(radar, tif_file, beam_width=1.0,
                                 az_start=0.0, az_end=360.0, az_size=360,
                                 elev_start=0.0, elev_end=90.0,
                                 elev_size=90):
    """
    Lowest Elevation No Blockage Calculation

    Parameters
    ----------
    radar : Radar
        Radar object used.
    tif_file : string
        Name of geotiff file to use for the
        calculation.

    Other Parameters
    ----------------
    beam_width : float
        Radar's beam width for calculation.
        Default value is 1.0.
    az_start : float
        Azimuth to start calculation at. Default is 0.0 degrees.
    az_end: float
        Azimuth to end calculation at. Default is 360.0 degrees.
    az_size: int
        Number of azimuth values between az_start and az_end. This can
        also be seen as spacing. az_start=0.0, az_end=360.0 and az_size=360
        is 1 degree spacing. Default is 360.
    elev_start : float
        Elevation angle to start the calculation at. Default value is
        0.0.
    elev_end : float
        Elevation angle to end the calculation at. Default value is
        90.0.
    elev_size : int
        Number of elevation values between elev_start and elev_end.
        Default value is 90.
    Returns
    -------
    low_el_not_blocked_all : array
        Array of elevation angles for all azimuths when less than 0.01 CBB
        fraction is achieved.

    Note
    ----
    Because the calculation creates an rhi for each azimuth, the
    calculation can take a decent amount of time. For example,
    360 azimuths with 300 elevations between 0-90 degrees and 1400
    gates, takes about 6 minutes to run. Working on ways to speed
    the calculation up.

    """

    # Define needed values for the temporary rhi radar.
    low_el_list = []
    azimuths = np.linspace(az_start, az_end, az_size)
    ngates = radar.ngates
    _range = radar.range['data']
    lat = radar.latitude['data']
    lon = radar.longitude['data']
    alt = radar.altitude['data']

    # Take all azimuths and create an rhi for each slice to
    # calculate all elevations at all gates.
    for azimuth in azimuths:
        rhi_radar = pyart.testing.make_empty_rhi_radar(
            ngates, elev_size, 1)
        rhi_radar.latitude['data'] = lat
        rhi_radar.longitude['data'] = lon
        rhi_radar.altitude['data'] = alt
        rhi_radar.range['data'] = _range
        rhi_radar.elevation['data'] = np.linspace(
            elev_start, elev_end, elev_size)
        rhi_radar.azimuth['data'] = np.array([azimuth] * elev_size)

        # Calculate beam blockage using the values from the rhi radar.
        cbb = beam_block(rhi_radar, tif_file, beam_width)[1]

        # Finds the minimum elevation at each gate by taking all the
        # above gates and when less than 0.01 CBB fraction is achieved
        # that gates index is matched with the elevation index to obtain
        # elevation and puts it into an array.
        not_blocked_lowest = []
        shape = (1, ngates)
        one_az = np.ones(shape)
        for i in range(len(_range)):
            not_blocked = np.argwhere(cbb[:, i] < 0.01)
            not_blocked_lowest.append(not_blocked.min())
            one_az[0, i] = rhi_radar.elevation[
                'data'][not_blocked_lowest[i]]
        # Puts all the elevation data into a list.
        low_el_list.append(one_az)

        # Deletes the rhi radar after it is used to save memory.
        del rhi_radar
    # Puts all the elevations from each azimuth together.
    low_el_not_blocked_all = np.concatenate(low_el_list)
    return low_el_not_blocked_all
