# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t; python-indent: 4 -*-
#
# =============================================================================
# Copyright (©) 2015-2017 LCS
# Laboratoire Catalyse et Spectrochimie, Caen, France.
#
# This software is a computer program whose purpose is to [describe
# functionalities and technical features of your software].
#
# This software is governed by the CeCILL license under French law and
# abiding by the rules of distribution of free software. You can use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty and the software's author, the holder of the
# economic rights, and the successive licensors have only limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading, using, modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean that it is complicated to manipulate, and that also
# therefore means that it is reserved for developers and experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and, more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.
# =============================================================================


"""

"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from spectrochempy.api import ur, set_nmr_context, quantity

def test_ppm():

    x = 1 * ur.ppm
    assert x.units == ur.ppm

def test_nmr_context():

    #print('\n')
    set_nmr_context(larmor=104.3 * ur.MHz)

    fhz = 10000 * ur.Hz
    with ur.context('nmr'):
        fppm = fhz.to('ppm')

    assert "{:~.3f}".format(fppm) == '95.877 ppm'

    with ur.context('nmr'):
        fhz = fppm.to('Hz')

    assert "{:~.3f}".format(fhz) == '10000.000 Hz'


def test_units():

    assert 10 * ur.km == 10000 * ur.m

    assert ur.km / ur.m == 1000.

    x = (ur.km / ur.m)
    assert x.dimensionless

    assert type(x) == type(ur.km)

def test_repr_html():
    a = quantity(10, 's/km')
    assert "{}".format(a) == "10 second / kilometer"
    assert a._repr_html_() == "10 s.km<sup>-1</sup>"
    #print(a)

def test_unit_dimensionality():
    a = quantity(1., 'cm')
    b = a/quantity(1., 'km')
    #print(b)
