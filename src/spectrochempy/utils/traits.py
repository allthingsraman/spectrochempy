# ======================================================================================
# Copyright (©) 2015-2025 LCS - Laboratoire Catalyse et Spectrochimie, Caen, France.
# CeCILL-B FREE SOFTWARE LICENSE AGREEMENT
# See full LICENSE agreement in the root directory.
# ======================================================================================
import inspect

import traitlets as tr

from spectrochempy.extern.traittypes import Empty
from spectrochempy.extern.traittypes import SciType


class SpectroChemPyType(SciType):
    """A SpectroChemPy trait type."""

    info_text = "a Spectrochempy object"

    klass = None

    def validate(self, obj, value):
        if value is None and not self.allow_none:
            self.error(obj, value)
        if value is None or value is tr.Undefined:
            return super().validate(obj, value)
        try:
            value = self.klass(value)
        except (ValueError, TypeError) as e:
            raise tr.TraitError(e) from None
        return super().validate(obj, value)

    def set(self, obj, value):
        new_value = self._validate(obj, value)
        old_value = obj._trait_values.get(self.name, self.default_value)
        obj._trait_values[self.name] = new_value
        if (
            (old_value is None and new_value is not None)
            or (old_value is tr.Undefined and new_value is not tr.Undefined)
            or old_value != new_value
        ):
            obj._notify_trait(self.name, old_value, new_value)

    def __init__(self, default_value=Empty, allow_none=False, klass=None, **kwargs):
        if klass is None:
            klass = self.klass
        if (klass is not None) and inspect.isclass(klass):
            self.klass = klass
        else:
            raise tr.TraitError(f"The klass attribute must be a class not: {klass!r}")
        if default_value is Empty:
            default_value = klass()
        elif default_value is not None and default_value is not tr.Undefined:
            default_value = klass(default_value)
        super().__init__(default_value=default_value, allow_none=allow_none, **kwargs)

    def make_dynamic_default(self):
        if self.default_value is None or self.default_value is tr.Undefined:
            return self.default_value
        return self.default_value.copy()


class NDDatasetType(SpectroChemPyType):
    """A NDDataset trait type."""

    info_text = "a SpectroChemPy NDDataset"

    def __init__(self, default_value=Empty, allow_none=False, dtype=None, **kwargs):
        if "klass" not in kwargs and self.klass is None:
            from spectrochempy.core.dataset.nddataset import NDDataset

            kwargs["klass"] = NDDataset
        super().__init__(
            default_value=default_value,
            allow_none=allow_none,
            **kwargs,
        )
        self.metadata.update({"dtype": dtype})


class CoordType(SpectroChemPyType):
    """A NDDataset trait type."""

    info_text = "a SpectroChemPy coordinates object"

    def __init__(self, default_value=Empty, allow_none=False, dtype=None, **kwargs):
        if "klass" not in kwargs and self.klass is None:
            from spectrochempy.core.dataset.coord import Coord

            kwargs["klass"] = Coord
        super().__init__(default_value=default_value, allow_none=allow_none, **kwargs)
        self.metadata.update({"dtype": dtype})


class PositiveInteger(tr.Integer):
    """A trait for positive integer values."""

    info_text = "a positive integer"
    default_value = 0

    def validate(self, obj, value):
        if value is None and not self.allow_none:
            self.error(obj, value)
        if (value is None or value is tr.Undefined) and self.allow_none:
            return value
        if value is None or value is tr.Undefined:
            return super().validate(obj, value)
        if value < 0:
            self.error(obj, value)
        return super().validate(obj, value)


class PositiveOddInteger(tr.Integer):
    """A trait for positive odd integer values."""

    info_text = "a positive odd integer"
    default_value = 1

    def validate(self, obj, value):
        if value is None and not self.allow_none:
            self.error(obj, value)
        if (value is None or value is tr.Undefined) and self.allow_none:
            return value
        if value is None or value is tr.Undefined:
            return super().validate(obj, value)
        if value < 0 or value % 2 == 0:
            self.error(obj, value)
        return super().validate(obj, value)
