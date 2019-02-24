# -*- coding: utf-8 -*-
#
# ======================================================================================================================
# Copyright (©) 2015-2019 LCS
# Laboratoire Catalyse et Spectrochimie, Caen, France.
# CeCILL-B FREE SOFTWARE LICENSE AGREEMENT
# See full LICENSE agreement in the root directory
# ======================================================================================================================


"""Plugin module to perform automatic subtraction of ref on a dataset.

"""
__all__ = ['autosub']

__dataset_methods__ = __all__

# ----------------------------------------------------------------------------------------------------------------------
# third party imports
# ----------------------------------------------------------------------------------------------------------------------

import numpy as np
from scipy.optimize import minimize_scalar
from numba import jit

# ----------------------------------------------------------------------------------------------------------------------
# localimports
# ----------------------------------------------------------------------------------------------------------------------

import matplotlib.pyplot as plt
from spectrochempy.core.dataset.ndcoords import CoordRange


def autosub(dataset, ref, *ranges, dim='x', method='chi2', inplace=False):
    """Automatic subtraction of ref to the dataset to minimise peaks due to ref

    Parameters
    -----------
    dataset : |NDDataset|.
        Dataset to which we want to subtract the reference data

    ref : |NDDataset|.
         1D reference data, with a size maching the axis to subtract
         (axis parameter) #TODO : optionally use title of axis

    xrange : pair(s) of values. Any number of pairs is allowed.
        Coord range(s) in which the variance is minimized

    inplace : `bool`, optional, default = False.
        True if the subtraction is done in place.
        In this case we do not need to catch the function output

    dim : str or int [optional, default = 'x].
        Tells on which dimension to perform the subtraction. If dim is an integer it refers to the axis index.

    method  : str [optional, default = 'vardiff'].


    Returns
    --------
    out : |NDDataset|.
        The subtracted dataset

    Examples
    ---------

    >>> import os
    >>> from spectrochempy import * #doctest: +ELLIPSIS
    <BLANKLINE>
    ...
    <BLANKLINE>
    >>> path_A = 'irdata/nh4y-activation.spg'
    >>> A = NDDataset.load(path_A, protocol='omnic')
    >>> ref = A[:,0]  # let's subtrack the first column
    >>> B = A.autosub(ref, [3900., 3700.], [1600., 1500.], inplace=False)
    >>> B #doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
    NDDataset: [[...]] a.u.

    """

    # output dataset

    if not inplace:
        new = dataset.copy()
    else:
        new = dataset

    # we assume that the last dimension ('x' for o transpopsed array) is always the dimension to which we want
    # to subtract.

    # Swap the axes to be sure to be in this situation
    axis = new.get_axis(dim)

    if axis == new.ndim - 1:
        axis = -1

    try:
        ref.to(dataset.units)
    except:
        raise ValueError('Units of the dataset and reference are not compatible')

    swaped = False
    if axis != -1:
        new = new.swapaxes(axis, -1)
        swaped = True

    # TODO: detect the case where the ref is not exactly
    # with same coords: interpolate?

    # selection of the multiple ranges

    shape = list(new.shape)
    ranges = tuple(np.array(ranges, dtype=float))
    # must be float to be considered as frequency for instance

    coords = new.coords[-1]
    xrange = CoordRange(*ranges, reversed=coords.reversed)

    s = []
    r = []

    # TODO: this do not work obviously for axis != -1 - correct this
    for xpair in xrange:
        # determine the slices

        sl = slice(*xpair)
        s.append(dataset[..., sl].data)
        r.append(ref[..., sl].data)

    X_r = np.concatenate((*s,), axis=-1)
    ref_r = np.concatenate((*r,), axis=-1).squeeze()

    indices, _ = list(zip(*np.ndenumerate(X_r[..., 0])))  # .squeeze())))

    # two methods
    # @jit
    def f_(alpha, p):
        if method == 'chi2':
            return np.sum((p - alpha * ref_r) ** 2)
        else:
            return np.var(np.diff(p - alpha * ref_r))

    @jit(cache=True)
    def minim():
        # table of subtraction coefficients
        x = []

        for tup in indices:
            # slices = [i for i in tup]
            # slices.append(slice(None))
            # args = (X_r[slices],)
            args = X_r[tup]
            res = minimize_scalar(f_, args=(args,), method='brent')
            x.append(res.x)

        x = np.asarray(x)
        return x

    x = minim()

    new._data -= np.dot(x.reshape(-1, 1), ref.data.reshape(1, -1))

    if swaped:
        new = new.swapaxes(axis, -1)

    new.history = str(
        new.modified) + ': ' + 'Automatic subtraction of :' + ref.name + '\n'

    return new
