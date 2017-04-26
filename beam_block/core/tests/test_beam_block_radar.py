""" Unit Tests for Beam Block's core/beam_block_radar.py module. """

import pyart
from numpy.testing import assert_almost_equal

import beam_block


def test_beam_block():
    """ Unit test for the beam_block_radar.beam_block function. """
    radar = pyart.io.read(beam_block.testing.SAMPLE_RADAR_NC_FILE)
    tif_file = beam_block.testing.SAMPLE_TIF_FILE
    beam_width = 1.0

    radar_bb_data = pyart.io.read(
        beam_block.testing.SAMPLE_RADAR_BLOCK_DATA_FILE)
    pbb_existing = radar_bb_data.fields['partial_beam_block']['data']
    cbb_existing = radar_bb_data.fields['cumulative_beam_block']['data']

    pbb_all, cbb_all = beam_block.core.beam_block(
        radar, tif_file, beam_width)

    assert_almost_equal(pbb_all, pbb_existing, 3)
    assert_almost_equal(cbb_all, cbb_existing, 3)

def test_beam_block_flags():
    """ Unit test for the beam_block_radar.beam_block_flags function. """
    radar_bb_data = pyart.io.read(
        beam_block.testing.SAMPLE_RADAR_BLOCK_DATA_FILE)
    pbb_existing = radar_bb_data.fields['partial_beam_block']['data']
    cbb_existing = radar_bb_data.fields['cumulative_beam_block']['data']

    pbb_flags_existing = radar_bb_data.fields[
        'partial_beam_block_flags']['data']
    cbb_flags_existing = radar_bb_data.fields[
        'cumulative_beam_block_flags']['data']
    no_block_thresh = 0.01
    complete_block_thresh = 0.95

    pbb_flags, cbb_flags = beam_block.core.beam_block_flags(
        pbb_existing, cbb_existing, no_block_thresh,
        complete_block_thresh)

    assert_almost_equal(pbb_flags, pbb_flags_existing, 3)
    assert_almost_equal(cbb_flags, cbb_flags_existing, 3)
