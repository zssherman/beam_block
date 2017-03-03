#!/usr/bin/env python
"""Beam Block

Beam Block is code for ARM that takes radar data, terrain data, and by
utilizing the tools Py-ART and Wradlib, retrieves partial beam block fraction
(PBB), cumulative beam block fraction (CBB), and flags for both.

"""


DOCLINES = __doc__.split("\n")

import os
import sys
import glob

from numpy.distutils.core import setup
from numpy.distutils.misc_util import Configuration

NAME = 'beam_block'
MAINTAINER = 'Zach Sherman'
DESCRIPTION = DOCLINES[0]
# INSTALL_REQUIRES = ['pyart', 'wradlib']
LONG_DESCRIPTION = "\n".join(DOCLINES[2:])
LICENSE = 'BSD'
PLATFORMS = "Linux"
MAJOR = 0
MINOR = 1
MICRO = 0
SCRIPTS = glob.glob('scripts/*')
TEST_SUITE = 'nose.collector'
TESTS_REQUIRE = ['nose']
VERSION = '%d.%d.%d' % (MAJOR, MINOR, MICRO)

def configuration(parent_package='', top_path=None):
    config = Configuration(None, parent_package, top_path)
    config.set_options(ignore_setup_xxx_py=True,
                       assume_default_configuration=True,
                       delegate_options_to_subpackages=True,
                       quiet=True)

    config.add_subpackage('beam_block')

    return config


def setup_package():

    setup(
        name=NAME,
        maintainer=MAINTAINER,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        version=VERSION,
        license=LICENSE,
        platforms=PLATFORMS,
        configuration=configuration,
        include_package_data=True,
      #  install_requires=INSTALL_REQUIRES,
        test_suite=TEST_SUITE,
        tests_require=TESTS_REQUIRE,
        scripts=SCRIPTS,
    )

if __name__ == '__main__':
    setup_package()
