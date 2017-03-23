""" Setup for Beam Block Subpackages. """

from numpy.distutils.core import setup
from numpy.distutils.misc_util import Configuration

def configuration(parent_package='', top_path=None):
    """ Configuration of beam_block subpackages. """
    config = Configuration('beam_block', parent_package, top_path)
    config.add_subpackage('config')
    config.add_subpackage('core')
    return config

if __name__ == '__main__':
    setup(**configuration(top_path='').todict())
