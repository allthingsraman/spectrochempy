# # -*- coding: utf-8 -*-
# # ======================================================================================
# # Copyright (©) 2015-2023 LCS - Laboratoire Catalyse et Spectrochimie, Caen, France.
# # CeCILL-B FREE SOFTWARE LICENSE AGREEMENT
# # See full LICENSE agreement in the root directory.
# # ======================================================================================
# flake8: noqa

from os import environ

import numpy as np
import pytest
import traitlets as tr

import spectrochempy as scp
from spectrochempy.analysis._base import (
    AnalysisConfigurable,
    DecompositionAnalysis,
    LinearRegressionAnalysis,
    NotFittedError,
)
from spectrochempy.utils import docstrings as chd


# test docstring
# but this is not intended to work with the debugger - use run instead of debug!
@pytest.mark.skipif(
    environ.get("PYDEVD_LOAD_VALUES_ASYNC", None),
    reason="debug mode cause error when checking docstrings",
)
def test_base_docstrings():
    chd.PRIVATE_CLASSES = []  # do not test private class docstring
    module = "spectrochempy.analysis._base"

    # analyse AnalysisConfigurable
    chd.check_docstrings(
        module,
        obj=scp.analysis._base.AnalysisConfigurable,
        # exclude some errors - remove whatever you want to check
        exclude=["SA01", "EX01", "ES01", "GL11", "GL08", "PR01"],
    )

    # analyse DecompositionAnalysis
    chd.check_docstrings(
        module,
        obj=scp.analysis._base.DecompositionAnalysis,
        exclude=["SA01", "EX01", "ES01", "GL11", "GL08", "PR01"],
    )

    # analyse LinearRegressionAnalysis
    chd.check_docstrings(
        module,
        obj=scp.analysis._base.LinearRegressionAnalysis,
        exclude=["SA01", "EX01", "ES01", "GL11", "GL08", "PR01"],
    )


def test_analysisconfigurable():
    class Foo(AnalysisConfigurable):
        a = tr.Integer(None, allow_none=True, help="trait a").tag(config=True)
        b = tr.Unicode("foo_b", help="this is a trait b").tag(config=True)

    foo = Foo()
    assert isinstance(foo, AnalysisConfigurable)
    assert foo.name == "Foo"
    assert isinstance(foo.parent, tr.config.Application)
    assert foo.a is None
    # assert foo.help.startswith("Foo.a : Int\n")
    assert foo.traits()["b"].help == "this is a trait b"
    assert foo.config["Foo"] == {}, "not initialized"
    # assert foo.log == ""

    with pytest.raises(tr.TraitError):
        # not an integer
        foo.a = 10.1

    # set conf. at init
    foo.reset()  # needed to delete json (in case it was already created)
    cd = scp.app.config_dir
    assert not (cd / "Foo.json").exists()
    foo = Foo(a=1)
    assert foo.a == 1
    assert (cd / "Foo.json").exists()

    # wrong parameters
    with pytest.raises(KeyError):
        _ = Foo(j=1)

    # with


def test_analysisconfigurable_validation():
    class Foo(AnalysisConfigurable):
        """a test for mask"""

        def _fit(self, X):
            return X

    # case of 2D array (the classical case for decomposition problems)
    foo = Foo()
    assert foo.name == "Foo"
    with pytest.raises(NotFittedError):
        _ = foo.X

    X = [[1, 2], [2, 2], [1, 3]]
    foo.fit(X)
    assert foo.X._implements("NDDataset")
    X1 = foo.X
    X1[1, 0] = scp.MASKED  # this mask both row 1 and column 0
    assert np.all(X1.mask == [[True, False], [True, True], [True, False]])
    foo.fit(X1)

    # resulting X should have the same mask
    assert np.all(foo.X.mask == X1.mask)

    # 1D X
    X = [1.0, 2.0, 3.0]
    foo.fit(X)
    # A column has been added
    assert repr(foo.X) == "NDDataset: [float64] unitless (shape: (y:1, x:3))"

    X = scp.NDDataset(np.arange(3) + 1.5, coordset=[range(3)], units="m")
    foo.fit(X)
    assert repr(foo.X) == "NDDataset: [float64] m (shape: (y:1, x:3))"

    X = scp.NDDataset(np.arange(3) + 1.5, coordset=[range(3)], units="m")
    # with a mask
    X[1] = scp.MASKED
    foo.fit(X)
    assert repr(foo.X) == "NDDataset: [float64] m (shape: (y:1, x:3))"


# def test_decompositionanalysis():
#
#     X = scp.NDDataset(np.arange(3) + 1.5, coordset=[range(3)], units="m")
#     # with a mask
#     foo.fit(X)
#     assert repr(foo.X) == "NDDataset: [float64] m (shape: (y:1, x:3))"