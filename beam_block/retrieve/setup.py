""" Setup for Retrieve Subpackage. """

from numpy.distutils.core import setup
from numpy.distutils.misc_util import Configuration

def configuration(parent_package='', top_path=None):
    """ Configuration of retrieve subpackages. """
    config = Configuration('retrieve', parent_package, top_path)
    config.add_data_dir('tests')
    return config

if __name__ == '__main__':
    setup(**configuration(top_path='').todict())
