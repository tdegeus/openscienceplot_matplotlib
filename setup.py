
from setuptools import setup
import re

filepath = 'openscienceplot_matplotlib/__init__.py'
__version__ = re.findall(r'__version__ = \'(.*)\'', open(filepath).read())[0]

setup(
    name='openscienceplot_matplotlib',
    version=__version__,
    author='Tom de Geus',
    author_email='tom@geus.me',
    url='https://github.com/tdegeus/openscienceplot_matplotlib',
    keywords='matplotlib, hdf5, h5py',
    description='Store data from a matplotlib plot.',
    long_description='Store data from a matplotlib plot.',
    license='MIT',
    install_requires=['matplotlib', 'numpy', 'h5py'],
    packages=['openscienceplot_matplotlib'],
)
