# ======================================================================================
# Copyright (©) 2015-2025 LCS - Laboratoire Catalyse et Spectrochimie, Caen, France.
# CeCILL-B FREE SOFTWARE LICENSE AGREEMENT
# See full LICENSE agreement in the root directory.
# ======================================================================================
"""In this module, methods are provided to download external datasets from public database."""

__all__ = ["load_iris", "download_nist_ir"]
__dataset_methods__ = __all__

from pathlib import Path

import requests

from spectrochempy.application.application import error_
from spectrochempy.application.application import info_
from spectrochempy.core.dataset.coord import Coord
from spectrochempy.core.dataset.nddataset import NDDataset
from spectrochempy.core.readers.read_jcamp import read_jcamp
from spectrochempy.utils.typeutils import is_iterable


def load_iris():
    """
    Upload the classical "iris" dataset.

    The "IRIS" dataset is a classical example for machine learning.
    It is read from the `scikit-learn` package.

    Returns
    -------
    dataset
        The `IRIS` dataset.

    See Also
    --------
    read : Read data from experimental data.

    """
    from sklearn.datasets import load_iris as sklearn_iris

    data = sklearn_iris()

    coordx = Coord(
        labels=["sepal_length", "sepal width", "petal_length", "petal_width"],
        title="features",
    )
    labels = [data.target_names[i] for i in data.target]
    coordy = Coord(labels=labels, title="samples")

    new = NDDataset(
        data.data,
        coordset=[coordy, coordx],
        title="size",
        name="`IRIS` Dataset",
        units="cm",
    )

    new.history = "Loaded from scikit-learn datasets"

    return new


def download_nist_ir(CAS, index="all"):
    """
    Upload IR spectra from NIST webbook.

    Parameters
    ----------
    CAS : int or str
        the CAS number, can be given as "XXXX-XX-X" (str), "XXXXXXX" (str), XXXXXXX (int)

    index : str or int or tuple of ints
        If set to 'all' (default, import all available spectra for the compound
        corresponding to the index, or a single spectrum, or selected spectra.

    Returns
    -------
    list of NDDataset or NDDataset
        The dataset(s).

    See Also
    --------
    read : Read data from experimental data.

    """
    info_("download_nist_ir")
    if isinstance(CAS, str) and "-" in CAS:
        CAS = CAS.replace("-", "")

    if index == "all":
        # test urls and return list if any...
        index = []
        i = 0
        while "continue":
            url = (
                f"https://webbook.nist.gov/cgi/cbook.cgi?JCAMP=C{CAS}&Index={i}&Type=IR"
            )
            try:
                response = requests.get(url, timeout=10)
                if b"Spectrum not found" in response.content[:30]:
                    break
                index.append(i)
                i += 1
            except OSError:
                raise OSError("Cannot connect to the NIST server... ") from None

        if len(index) == 0:
            error_(IOError, "NIST IR: no spectrum found")
            return None
        if len(index) == 1:
            info_("NIST IR: 1 spectrum found")
        else:
            info_("NISTR IR: {len(index)} spectra found")

    elif isinstance(index, int):
        index = [index]
    elif not is_iterable(index):
        raise ValueError("index must be 'all', int or iterable of int")

    out = []
    for i in index:
        # sample adress (water, spectrum 1)
        # https://webbook.nist.gov/cgi/cbook.cgi?JCAMP=C7732185&Index=1&Type=IR
        url = f"https://webbook.nist.gov/cgi/cbook.cgi?JCAMP=C{CAS}&Index={i}&Type=IR"
        try:
            response = requests.get(url, stream=True, timeout=10)
            if b"Spectrum not found" in response.content[:30]:
                error_(
                    IOError,
                    f"NIST IR: Spectrum {i} does not exist... please check !",
                )
                if i == index[-1] and out == []:
                    return None
                break

        except OSError:
            error_("OSError: Cannot connect... ")
            return None

        # Load data
        txtdata = ""
        for rd in response.iter_content():
            txtdata += rd.decode("utf8")

        with open("temp.jdx", "w") as f:
            f.write(txtdata)
        try:
            ds = read_jcamp("temp.jdx")

            # replace the default entry ":imported from jdx file":
            ds.history[0] = f"Downloaded from NIST: {url}"
            out.append(ds)
            (Path() / "temp.jdx").unlink()

        except Exception:
            raise OSError(
                "Can't read this JCAMP file: please report the issue to Spectrochempy developpers",
            ) from None

    if len(out) == 1:
        return out[0]
    return out
