"""
=============================
Core (:mod:`beam_block.core`)
=============================

.. currentmodule:: beam_block.core

Core Beam Block function for retrieving beam block fractions and flags.

Core Functions
==============

.. autosummary::
    :toctree: generated/

    beam_block_radar
    beam_block_radar_flags
    beam_block_json
    beam_block_json_flags

"""

from .beam_block_radar import beam_block_radar, beam_block_radar_flags
from .beam_block_json import beam_block_json, beam_block_json_flags

__all__ = [s for s in dir() if not s.startswith('_')]
