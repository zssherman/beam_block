""" Unit Tests for Beam Block's config/dict_config.py module. """

import pyart
from numpy.testing import assert_almost_equal

import beam_block
from beam_block.config import dict_config


radar = pyart.io.read(beam_block.testing.SAMPLE_RADAR_NC_FILE)
radar_bb_data = pyart.io.read(beam_block.testing.SAMPLE_RADAR_BLOCK_DATA_FILE)

pbb_all = radar_bb_data.fields['partial_beam_block']['data']
cbb_all = radar_bb_data.fields['cumulative_beam_block']['data']
pbb_flags = radar_bb_data.fields['partial_beam_block_flag']['data']
cbb_flags = radar_bb_data.fields['cumulative_beam_block_flag']['data']

pbb_dict = dict_config.pbb_to_dict(pbb_all)
cbb_dict = dict_config.cbb_to_dict(cbb_all)

pbb_flags_dict = dict_config.pbb_flags_to_dict(pbb_flags)
cbb_flags_dict = dict_config.cbb_flags_to_dict(cbb_flags)


def test_pbb_to_dict():
    """ Unit test for the dict_config.pbb_to_dict function. """
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
    assert 'standard_name' in pbb_flags_dict 
    assert 'long_name' in pbb_flags_dict
    assert 'data' in pbb_flags_dict
    assert 'units' in pbb_flags_dict
    assert 'comment' in pbb_flags_dict
    assert pbb_flags_dict['data'].shape == (360, 360)
    assert_almost_equal(pbb_flags_dict['data'], pbb_flags, 3)


def test_cbb_flags_to_dict():
    """ Unit test for the dict_config.cbb_flags_to_dict function. """
    assert 'standard_name' in cbb_flags_dict
    assert 'long_name' in cbb_flags_dict
    assert 'data' in cbb_flags_dict
    assert 'units' in cbb_flags_dict
    assert 'comment' in cbb_flags_dict
    assert cbb_flags_dict['data'].shape == (360, 360)
    assert_almost_equal(cbb_flags_dict['data'], cbb_flags, 3)
