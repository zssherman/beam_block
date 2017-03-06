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
    beam_block_json

"""

from .beam_block_radar import beam_block_radar
from .beam_block_json import beam_block_json

__all__ = [s for s in dir() if not s.startswith('_')]
