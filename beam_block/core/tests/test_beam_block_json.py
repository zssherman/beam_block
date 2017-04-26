""" Unit Tests for Beam Block's core/beam_block_json.py module. """

import json
import pyart
from numpy.testing import assert_almost_equal

import beam_block


def test_json_beam_block():
    """ Unit test for the beam_block_json.json_beam_block function. """
    json_file = beam_block.testing.SAMPLE_RADAR_JSON_FILE
    with open(json_file) as data:
        json_data = json.load(data)

    tif_file = beam_block.testing.SAMPLE_TIF_FILE
    beam_width = 1.0

    radar_bb_data = pyart.io.read(
        beam_block.testing.SAMPLE_RADAR_BLOCK_DATA_FILE)
    pbb_existing = radar_bb_data.fields['partial_beam_block']['data']
    cbb_existing = radar_bb_data.fields['cumulative_beam_block']['data']

    pbb_all, cbb_all = beam_block.core.json_beam_block(
        json_data, tif_file, beam_width)

    assert_almost_equal(pbb_all, pbb_existing, 3)
    assert_almost_equal(cbb_all, cbb_existing, 3)
