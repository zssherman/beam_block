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

    beam_block
    beam_block_flags

"""

from .beam_block_radar import beam_block, beam_block_flags

__all__ = [s for s in dir() if not s.startswith('_')]
