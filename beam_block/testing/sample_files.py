"""
beam_block.testing.sample_files

Sample files needed to run the unit tests for the beam_block functions.

Note: This code was adapted from Py-ART's pyart.testing.sample_files.

.. autosummary::
    :toctree:generated/

    SAMPLE_TIF_FILE
    SAMPLE_RADAR_NC_FILE
    SAMPLE_RADAR_JSON_FILE
    SAMPLE_RADAR_JSON_TO_NC_FILE
    SAMPLE_RADAR_BLOCK_DATA_FILE
    SAMPLE_RADAR_LOW_ELEV_FILE

"""

import os

DATA_PATH = os.path.join(os.path.dirname(__file__), 'data')

SAMPLE_TIF_FILE = os.path.join(DATA_PATH, 'dtm_gra.tif')
SAMPLE_RADAR_NC_FILE = os.path.join(DATA_PATH, 'sample_radar.nc')
SAMPLE_RADAR_JSON_FILE = os.path.join(DATA_PATH, 'sample_json.json')
SAMPLE_RADAR_JSON_TO_NC_FILE = os.path.join(
    DATA_PATH, 'sample_out_radar_from_json.nc')
SAMPLE_RADAR_BLOCK_DATA_FILE = os.path.join(
    DATA_PATH, 'sample_out_radar_with_beam_blockage.nc')
SAMPLE_RADAR_LOW_ELEV_FILE = os.path.join(
    DATA_PATH, 'sample_low_elev_radar.nc')
