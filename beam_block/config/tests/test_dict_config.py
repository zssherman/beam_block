""" Unit Tests for Beam Block's config/dict_config.py module. """

import pyart
from numpy.testing import assert_almost_equal

import beam_block
from beam_block.config import dict_config


radar_bb = pyart.io.read(beam_block.testing.SAMPLE_RADAR_BLOCK_DATA_FILE)
radar_low_elev = pyart.io.read(
    beam_block.testing.SAMPLE_RADAR_LOW_ELEV_FILE)

def test_pbb_to_dict():
    """ Unit test for the dict_config.pbb_to_dict function. """
    pbb_all = radar_bb.fields['partial_beam_block']['data']
    pbb_dict = dict_config.pbb_to_dict(pbb_all)
    assert 'standard_name' in pbb_dict
    assert 'long_name' in pbb_dict
    assert 'coordinates' in pbb_dict
    assert 'data' in pbb_dict
    assert 'units' in pbb_dict
    assert 'comment' in pbb_dict
    assert pbb_dict['data'].shape == (360, 360)
    assert_almost_equal(pbb_dict['data'], pbb_all, 3)


def test_cbb_to_dict():
    """ Unit test for the dict_config.cbb_to_dict function. """
    cbb_all = radar_bb.fields['cumulative_beam_block']['data']
    cbb_dict = dict_config.cbb_to_dict(cbb_all)
    assert 'standard_name' in cbb_dict
    assert 'long_name' in cbb_dict
    assert 'coordinates' in cbb_dict
    assert 'data' in cbb_dict
    assert 'units' in cbb_dict
    assert 'comment' in cbb_dict
    assert cbb_dict['data'].shape == (360, 360)
    assert_almost_equal(cbb_dict['data'], cbb_all, 3)


def test_pbb_flags_to_dict():
    """ Unit test for the dict_config.pbb_flags_to_dict function. """
    pbb_flags = radar_bb.fields['partial_beam_block_flags']['data']
    pbb_flags_dict = dict_config.pbb_flags_to_dict(pbb_flags)
    assert 'standard_name' in pbb_flags_dict
    assert 'long_name' in pbb_flags_dict
    assert 'data' in pbb_flags_dict
    assert 'units' in pbb_flags_dict
    assert 'notes' in pbb_flags_dict
    assert pbb_flags_dict['data'].shape == (360, 360)
    assert_almost_equal(pbb_flags_dict['data'], pbb_flags, 3)


def test_cbb_flags_to_dict():
    """ Unit test for the dict_config.cbb_flags_to_dict function. """
    cbb_flags = radar_bb.fields['cumulative_beam_block_flags']['data']
    cbb_flags_dict = dict_config.cbb_flags_to_dict(cbb_flags)
    assert 'standard_name' in cbb_flags_dict
    assert 'long_name' in cbb_flags_dict
    assert 'data' in cbb_flags_dict
    assert 'units' in cbb_flags_dict
    assert 'notes' in cbb_flags_dict
    assert cbb_flags_dict['data'].shape == (360, 360)
    assert_almost_equal(cbb_flags_dict['data'], cbb_flags, 3)


def test_lowest_el_not_blocked_to_dict():
    """ Unit test for the dict_config.lowest_el_not_blocked_to_dict
    function. """
    low_el_not_blocked_all = radar_low_elev.fields[
        'low_el_not_blocked']['data']
    low_el_not_blocked_dict = dict_config.lowest_el_not_blocked_to_dict(
        low_el_not_blocked_all)
    assert 'standard_name' in low_el_not_blocked_dict
    assert 'long_name' in low_el_not_blocked_dict
    assert 'data' in low_el_not_blocked_dict
    assert 'units' in low_el_not_blocked_dict
    assert 'comment' in low_el_not_blocked_dict
    assert low_el_not_blocked_dict['data'].shape == (360, 360)
    assert_almost_equal(
        low_el_not_blocked_dict['data'], low_el_not_blocked_all, 3)
