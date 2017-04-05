""" Unit Tests for Beam Block's retrieve/low_el_no_block.py module. """

import pyart
from numpy.testing import assert_almost_equal

import beam_block


def test_lowest_elevation_no_blockage():
    """ Unit test for the low_el_no_block.lowest_elevation_no_blockage
    function. """
    radar = pyart.io.read(beam_block.testing.SAMPLE_RADAR_NC_FILE)
    tif_file = beam_block.testing.SAMPLE_TIF_FILE
    beam_width = 1.0
    az_start = 0.0
    az_end = 360.0
    az_size = 360
    elev_start = 0.0
    elev_end = 90.0
    elev_size = 90

    radar_bb_data = pyart.io.read(
        beam_block.testing.SAMPLE_RADAR_LOW_ELEV_FILE)
    low_el_existing = radar_bb_data.fields['lowest_elev_not_blocked']['data']

    low_el_not_blocked_all = beam_block.retrieve.lowest_elevation_no_blockage(
        radar, tif_file, beam_width, az_start, az_end, az_size, elev_start,
        elev_end, elev_size)

    assert_almost_equal(low_el_not_blocked_all, low_el_existing, 3)
