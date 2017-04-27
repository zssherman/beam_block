"""
=================================
Core (:mod:`beam_block.retrieve`)
=================================

.. currentmodule:: beam_block.retrieve

Retrieve elevation function for retrieving lowest elevations needed
for a gate to achieve less than 0.01 CBB fraction.

Core Functions
==============

.. autosummary::
    :toctree: generated/

    lowest_elevation_no_blockage

"""

from .low_el_no_block import lowest_elevation_no_blockage

__all__ = [s for s in dir() if not s.startswith('_')]
