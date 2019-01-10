# -*- coding: utf-8 -*-
#
# =============================================================================
# Copyright (©) 2015-2019 LCS
# Laboratoire Catalyse et Spectrochimie, Caen, France.
# CeCILL-B FREE SOFTWARE LICENSE AGREEMENT  
# See full LICENSE agreement in the root directory
# =============================================================================


from spectrochempy import *

import pytest

def test_concatenate(IR_dataset_2D):

    dataset = IR_dataset_2D

    #print(dataset)
    s1 = dataset[:10]
    s2 = dataset[20:]

    # check with derived units
    s1.to(ur.m, force=True)
    s2.to(ur.dm, force=True)
    s = concatenate(s1, s2, axis=0)
    assert s.units==s1.units
    assert s.shape[0]==(s1.shape[0]+s2.shape[0])
    assert s.coordset(0).size==(s1.coordset(0).size+s2.coordset(0).size)
    s = s.sort(axis=0)
    s.plot()

    # second syntax
    s = s1.concatenate(s2, axis=0)
    assert s.units==s1.units
    assert s.shape[0]==(s1.shape[0]+s2.shape[0])
    assert s.coordset(0).size==(s1.coordset(0).size+s2.coordset(0).size)

    # third syntax
    s = concatenate((s1, s2), axis=0)
    assert s.units==s1.units
    assert s.shape[0]==(s1.shape[0]+s2.shape[0])
    assert s.coordset(0).size==(s1.coordset(0).size+s2.coordset(0).size)

def test_concatenate_1D_along_axis0(IR_dataset_2D):
    # TODO: very long process - try to optimize this
    dataset = IR_dataset_2D[3:]

    # make these data with a mask
    dataset[:, 1] = masked

    # split all rows
    rows = []
    for i in range(len(dataset)):
        rows.append(dataset[i])

    assert len(rows)==dataset.shape[0]

    # reconstruct

    new = stack(rows)
    assert new.shape == dataset.shape

    # now with uncertainty

    rows = []
    for i in range(len(dataset)):
        row = dataset[i]
        row._uncertainty = np.abs(row.data *.001)
        rows.append(row)

    assert len(rows)==dataset.shape[0]

    # reconstruct
    new = stack(rows)
    assert new.shape == dataset.shape

def test_concatenate_along_axis1(IR_dataset_2D):

    dataset = IR_dataset_2D

    coord = dataset.coordset(-1)

    # test along axis 1
    ranges = ([6000., 3500.], [1800., 1500.])

    ranges = CoordRange(*ranges, reversed=coord.reversed)

    s = []
    for pair in ranges:
        # determine the slices
        sl = slice(*pair)
        s.append(dataset[..., sl])

    sbase = concatenate( *s, axis=-1)
    xbase = sbase.coordset(-1)

    assert sbase.shape[-1] == (s[0].shape[-1] + s[1].shape[-1])
    assert xbase.size == (s[0].coordset(-1).size + s[1].coordset(-1).size)

    sbase.plot_stack()
    show()