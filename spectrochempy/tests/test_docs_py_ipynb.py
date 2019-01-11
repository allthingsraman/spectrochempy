#! python3
# -*- coding: utf-8 -*-
#
# =============================================================================
# Copyright (©) 2015-2019 LCS
# Laboratoire Catalyse et Spectrochimie, Caen, France.
# CeCILL-B FREE SOFTWARE LICENSE AGREEMENT 
# See full LICENSE agreement in the root directory
# =============================================================================



import pytest
from glob import glob
import os, sys

from spectrochempy.utils.testing import notebook_run, example_run

@pytest.mark.skip # problem with timeout
@pytest.mark.parametrize('notebook', glob("../docs/user/*/*.ipynb"))
def test_notebooks(notebook):
    if '.ipynb_checkpoints' in notebook :
        return True
    if os.path.exists(notebook) and os.path.splitext(notebook)[
        -1] == '.ipynb' :
        nb, errors = notebook_run(notebook)
        assert errors == []

@pytest.mark.parametrize('example', glob("../docs/user/examples/*/*.py"))
def test_example(example):
    if os.path.exists(example) and os.path.splitext(example)[-1] == '.py' :
        e, message, err = example_run(example)
        print(e, message.decode('utf8'), err )
        assert not e, message.decode('utf8')
