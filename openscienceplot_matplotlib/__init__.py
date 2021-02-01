'''
This module provides methods to save data from a matplotlib plot.

:dependencies:

    * numpy
    * matplotlib
    * h5py

:copyright:

    | Tom de Geus
    | tom@geus.me
    | http://www.geus.me
'''

import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import h5py


__version__ = '0.1.0'


def info():
    r'''
Return basic library information.
    '''

    return [
        'openscienceplot_matplotlib={0:s}'.format(__version__),
        'matplotlib={0:s}'.format(matplotlib.__version__)]


def write_h5py(data, key, handle):
    r'''
Save plot data to HDF5-file.

:arguments:

    **data** (``h5py.File``)
        Opened HDF5 file.

    **key** (``<str>``)
        Name of the dataset to which to write.

    **handle**
        The handle to write.
    '''

    import warnings

    if key == '/':
        raise IOError('Cannot write to root')

    if len(handle) == 1:
        handle = handle[0]

    if isinstance(handle, matplotlib.lines.Line2D):
        xy = handle.get_xydata()
        dset = data.create_dataset(key, xy.shape, dtype=xy.dtype)
        dset[:, :] = xy
        dset.attrs['artist'] = 'matplotlib.lines.Line2D'
        dset.attrs['color'] = handle.get_color()
        dset.attrs['linestyle'] = handle.get_linestyle()
        dset.attrs['marker'] = handle.get_marker()
        dset.attrs['label'] = handle.get_label()
        return

    if isinstance(handle, matplotlib.container.ErrorbarContainer):
        xy = handle[0].get_xydata()
        dset = data.create_dataset(key, xy.shape, dtype=xy.dtype)
        dset[:, :] = xy
        dset.attrs['artist'] = 'matplotlib.lines.Line2D'
        dset.attrs['color'] = handle[0].get_color()
        dset.attrs['linestyle'] = handle[0].get_linestyle()
        dset.attrs['marker'] = handle[0].get_marker()
        warnings.warn('Error-bars not saved, help wanted.', Warning)
        return

    raise IOError('Unknown handle. Please consider filing a bug-report.')


def restore_h5py(data, key, axis=None):
    r'''
Restore plot from HDF5-file.

:arguments:

    **data** (``h5py.File``)
        Opened HDF5 file.

    **key** (``<str>``)
        Name of the dataset from which to read.

:options:

    **axis** ([``plt.gca()``] | ...)
        Specify the axis on which to plot.

:returns:

    **handle**
        The handle of the created plot.
    '''

    if axis is None:
        plt.gca()

    dset = data[key]

    if dset.attrs['artist'] == 'matplotlib.lines.Line2D':

        xy = dset[...]
        opts = {}

        for key in ['color', 'linestyle', 'marker', 'label']:
            if key in dset.attrs:
                opts[key] = dset.attrs[key]

        return axis.plot(xy, **opts)

    raise IOError('Data-set not interpretable. Please consider filing a bug-report.')
