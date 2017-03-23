"""
beam_block.config.dict_config
=============================

Configuration of dictionarys.

Functions that take beam blockage data and creates
default dictionaries for each.

.. autosummary::
    :toctree: generated/

    pbb_to_dict
    cbb_to_dict
    pbb_flags_to_dict
    cbb_flags_to_dict
    lowest_el_not_blocked_to_dict

"""


def pbb_to_dict(pbb_all):
    """ Function that takes the pbb_all array and turns
    it into a dictionary to be used and added to the
    pyart radar object. """
    pbb_dict = {}
    pbb_dict['coordinates'] = 'elevation, azimuth, range'
    pbb_dict['units'] = 'unitless'
    pbb_dict['data'] = pbb_all
    pbb_dict['standard_name'] = 'partial_beam_block'
    pbb_dict['long_name'] = 'Partial Beam Block Fraction'
    pbb_dict['comment'] = 'Partial beam block fraction due to terrain.'
    return pbb_dict


def cbb_to_dict(cbb_all):
    """ Function that takes the cbb_all array and turns
    it into a dictionary to be used and added to the
    pyart radar object. """
    cbb_dict = {}
    cbb_dict['coordinates'] = 'elevation, azimuth, range'
    cbb_dict['units'] = 'unitless'
    cbb_dict['data'] = cbb_all
    cbb_dict['standard_name'] = 'cumulative_beam_block'
    cbb_dict['long_name'] = 'Cumulative Beam Block Fraction'
    cbb_dict['comment'] = 'Cumulative beam block fraction due to terrain.'
    return cbb_dict


def pbb_flags_to_dict(pbb_flags):
    """ Function that takes the pbb_flags array and
    turns it into a dictionary to be used and added
    to the pyart radar object. """
    pbb_flags_dict = {}
    pbb_flags_dict['units'] = 'unitless'
    pbb_flags_dict['data'] = pbb_flags
    pbb_flags_dict['standard_name'] = 'partial_beam_block_flag'
    pbb_flags_dict['long_name'] = 'Partial Beam Block Flag'
    pbb_flags_dict['comment'] = 'Partial beam block fraction flag, ' \
                               '1 for flagged values, 0 for non-flagged.'
    return pbb_flags_dict


def cbb_flags_to_dict(cbb_flags):
    """ Function that takes the cbb_flags array and
    turns it into a dictionary to be used and added
    to the pyart radar object. """
    cbb_flags_dict = {}
    cbb_flags_dict['units'] = 'unitless'
    cbb_flags_dict['data'] = cbb_flags
    cbb_flags_dict['standard_name'] = 'cumulative_beam_block_flag'
    cbb_flags_dict['long_name'] = 'Cumulative Beam Block Flag'
    cbb_flags_dict['comment'] = 'Cumulative beam block fraction flag, ' \
                               '1 for flagged values, 0 for non-flagged.'
    return cbb_flags_dict


def lowest_el_not_blocked_to_dict(low_el_not_blocked_all):
    """ Function that takes the low_el_not_blocked_all
    array and turns it into a dictionary to be used and
    added to the pyart radar object. """
    low_el_not_blocked_dict = {}
    low_el_not_blocked_dict['units'] = 'Degrees'
    low_el_not_blocked_dict['data'] = low_el_not_blocked_all
    low_el_not_blocked_dict['standard_name'] = 'low_el_not_blocked'
    low_el_not_blocked_dict['long_name'] = 'Lowest Elevation Not Blocked'
    low_el_not_blocked_dict['comment'] = 'Lowest elevation when each gate ' \
                                         'will achieve less than 0.01 CBB.'
    return low_el_not_blocked_dict
