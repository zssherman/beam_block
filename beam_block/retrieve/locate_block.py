"""
beam_block.retrieve.locate_block
================================

Functions that find where or where not beam blockage is occurring
and returns the ray and gate index value.

.. autosummary::
    :toctreeL generated/
    :template: dev_template.rst

    locate_block_pbb
    locate_block_cbb
    locate_no_block_pbb
    locate_no_block_cbb

"""

import numpy as np


def locate_block_pbb(pbb, pbb_threshold=0.01):
    """
    Finds location, ray gate, where partial beam blockage
    occurs above the given blockage threshold.

    Parameters
    ----------
    pbb : array
        Array of partial beam blockage values.
    pbb_threshold : float
        Value at which any ray gate above the value will be pulled.
        Default is 0.01.

    Returns
    -------
    location_block_pbb : array
        Array of ray gates where partial beam blockage is
        occurring, according to the threshold value.

    """

    location_block_pbb = np.argwhere(pbb > pbb_threshold)
    return location_block_pbb


def locate_block_cbb(cbb, cbb_threshold):
    """
    Finds location, ray gate, where cumulative beam blockage
    occurs above the given blockage threshold.

    Parameters
    ----------
    cbb : array
        Array of cumulative beam blockage values.
    cbb_threshold : float
        Value at which any ray gate above the value will be pulled.
        Default is 0.01.

    Returns
    -------
    location_block_cbb : array
        Array of ray gates where cumulative beam blockage is
        occurring, according to the threshold value.

    """

    location_block_cbb = np.argwhere(cbb > cbb_threshold)
    return location_block_cbb


def locate_no_block_pbb(pbb, pbb_threshold=0.01):
    """
    Finds location, ray gate, where partial beam blockage
    occurs below the given blockage threshold.

    Parameters
    ----------
    pbb : array
        Array of partial beam blockage values.
    pbb_threshold : float
        Value at which any ray gate below the value will be pulled.
        Default is 0.01.

    Returns
    -------
    location_no_block_pbb : array
        Array of ray gates where partial beam blockage is
        not occurring, according to the threshold value.

    """

    location_no_block_pbb = np.argwhere(pbb < pbb_threshold)
    return location_no_block_pbb


def locate_no_block_cbb(cbb, cbb_threshold):
    """
    Finds location, ray gate, where cumulative beam blockage
    occurs below the given blockage threshold.

    Parameters
    ----------
    cbb : array
        Array of cumulative beam blockage values.
    cbb_threshold : float
        Value at which any ray gate below the value will be pulled.
        Default is 0.01.

    Returns
    -------
    location_no_block_cbb : array
        Array of ray gates where cumulative beam blockage is
        not occurring, according to the threshold value.

    """

    location_no_block_cbb = np.argwhere(cbb < cbb_threshold)
    return location_no_block_cbb
