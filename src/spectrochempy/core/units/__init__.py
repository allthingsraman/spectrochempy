# ======================================================================================
# Copyright (©) 2015-2025 LCS - Laboratoire Catalyse et Spectrochimie, Caen, France.
# CeCILL-B FREE SOFTWARE LICENSE AGREEMENT
# See full LICENSE agreement in the root directory.
# ======================================================================================
# lazy_stub: skip
"""The core interface to the Pint library."""

__all__ = [
    "Unit",
    "Quantity",
    "ur",
    "set_nmr_context",  # TODO put this in the nmr plugin
    "DimensionalityError",
]

import warnings

from pint import __version__

# check pint version
pint_version = int(__version__.split(".")[1])
if pint_version < 20:
    raise ImportError(
        "Current pint version is {__version__} but must be 0.20 or higher. Please consider upgrading it "
        "(e.g. `> pip install pint --upgrade` or `> conda update pint` )\n",
    )
if pint_version < 24:
    warnings.warn(
        f"Warning: current pint version is {__version__}. It might not be supported by SpectroChemPy in the future.\n"
        f"Please consider upgrading it to 0.24 or higher (e.g. `> pip install pint --upgrade` or `> conda update pint`)\n",
        stacklevel=2,
    )

if pint_version < 24:
    from functools import wraps

    from pint import Context
    from pint import DimensionalityError
    from pint import Quantity
    from pint import Unit
    from pint import UnitRegistry
    from pint import __version__
    from pint import formatting
    from pint import set_application_registry
    from pint.facets.plain import ScaleConverter
    from pint.facets.plain import UnitDefinition
    from pint.util import UnitsContainer

    # ======================================================================================
    # Modify the pint behaviour
    # ======================================================================================
    formats = {
        "P": {  # Pretty format.
            "as_ratio": False,  # True in pint
            "single_denominator": False,
            "product_fmt": "·",
            "division_fmt": "/",
            "power_fmt": "{}{}",
            "parentheses_fmt": "({})",
            "exp_call": formatting._pretty_fmt_exponent,
        },
        "L": {  # Latex format.
            "as_ratio": False,  # True in pint
            "single_denominator": True,
            "product_fmt": r" \cdot ",
            "division_fmt": r"\frac[{}][{}]",
            "power_fmt": "{}^[{}]",
            "parentheses_fmt": r"\left({}\right)",
        },
        "H": {  # HTML format.
            "as_ratio": False,  # True in pint
            "single_denominator": False,
            "product_fmt": r" ",
            "division_fmt": r"{}/{}",
            "power_fmt": r"{}<sup>{}</sup>",
            "parentheses_fmt": r"({})",
        },
        "": {  # Default format.
            "as_ratio": True,
            "single_denominator": False,
            "product_fmt": " * ",
            "division_fmt": " / ",
            "power_fmt": "{} ** {}",
            "parentheses_fmt": r"({})",
        },
        "C": {  # Compact format.
            "as_ratio": False,
            "single_denominator": False,
            "product_fmt": "*",  # TODO: Should this just be ''?
            "division_fmt": "/",
            "power_fmt": "{}**{}",
            "parentheses_fmt": r"({})",
        },
        "K": {  # spectrochempy Compact format.
            "as_ratio": False,
            "single_denominator": False,
            "product_fmt": " ",
            "division_fmt": "/",
            "power_fmt": "{}^{}",
            "parentheses_fmt": r"({})",
        },
    }

    del formatting._FORMATTERS["P"]

    @formatting.register_unit_format("P")
    def format_pretty(unit, registry, **options):
        return formatting.formatter(
            unit.items(),
            as_ratio=False,
            single_denominator=False,
            product_fmt="⋅",
            division_fmt="/",
            power_fmt="{}{}",
            parentheses_fmt="({})",
            exp_call=formatting._pretty_fmt_exponent,
            **options,
        )

    @formatting.register_unit_format("K")
    def format_spectrochempy_compact(unit, registry, **options):
        return formatting.formatter(
            unit.items(),
            as_ratio=False,
            single_denominator=False,
            product_fmt=" ",
            division_fmt="/",
            power_fmt="{}^{}",
            parentheses_fmt=r"({})",
            **options,
        )

    del formatting._FORMATTERS["L"]

    @formatting.register_unit_format("L")
    def format_latex(unit, registry, **options):
        preprocessed = {
            r"\mathrm{{{}}}".format(u.replace("_", r"\_")): p for u, p in unit.items()
        }
        formatted = formatting.formatter(
            preprocessed.items(),
            as_ratio=False,
            single_denominator=True,
            product_fmt=r" \cdot ",
            division_fmt=r"\frac[{}][{}]",
            power_fmt="{}^[{}]",
            parentheses_fmt=r"\left({}\right)",
            **options,
        )
        return formatted.replace("[", "{").replace("]", "}")

    del formatting._FORMATTERS["H"]

    @formatting.register_unit_format("H")
    def format_html(unit, registry, **options):
        return formatting.formatter(
            unit.items(),
            as_ratio=False,
            single_denominator=True,
            product_fmt=r"⋅",
            division_fmt=r"{}/{}",
            power_fmt=r"{}<sup>{}</sup>",
            parentheses_fmt=r"({})",
            **options,
        )

    del formatting._FORMATTERS["D"]

    @formatting.register_unit_format("D")
    def format_default(unit, registry, **options):
        return formatting.formatter(
            unit.items(),
            as_ratio=False,
            single_denominator=False,
            product_fmt="*",
            division_fmt="/",
            power_fmt="{}^{}",
            parentheses_fmt=r"({})",
            **options,
        )

    del formatting._FORMATTERS["C"]

    @formatting.register_unit_format("C")
    def format_compact(unit, registry, **options):
        return formatting.formatter(
            unit.items(),
            as_ratio=False,
            single_denominator=False,
            product_fmt="*",
            division_fmt="/",
            power_fmt="{}**{}",
            parentheses_fmt=r"({})",
            **options,
        )

    def _repr_html_(cls):
        p = cls.__format__("~H")
        # attempt to solve a display problem in notebook (recent version of pint
        # have a strange way to handle HTML. For me it doesn't work
        return p.replace(r"\[", "").replace(r"\]", "").replace(r"\ ", " ")

    Quantity._repr_html_ = _repr_html_
    Quantity._repr_latex_ = lambda cls: "$" + cls.__format__("~L") + "$"

    # TODO: work on this latex format

    Unit.scaling = property(
        lambda u: u._REGISTRY.Quantity(1.0, u._units).to_base_units().magnitude,
    )

    # --------------------------------------------------------------------------------------
    def __format__(self, spec):  # noqa: N807
        # modify Pint unit __format__

        spec = formatting.extract_custom_flags(spec or self.default_format)
        if "~" in spec:
            if not self._units:
                return ""

            # Spectrochempy
            if self.dimensionless and "absorbance" not in self._units:
                if self._units == "ppm":
                    units = UnitsContainer({"ppm": 1})
                elif self._units in ["percent", "transmittance"]:
                    units = UnitsContainer({"%": 1})
                elif self._units == "weight_percent":
                    units = UnitsContainer({"wt.%": 1})
                elif self._units == "radian":
                    units = UnitsContainer({"rad": 1})
                elif self._units == "degree":
                    units = UnitsContainer({"deg": 1})
                # elif self._units == 'absorbance':
                #    units = UnitsContainer({'a.u.': 1})
                elif abs(self.scaling - 1.0) < 1.0e-10:
                    units = UnitsContainer({"": 1})
                else:
                    units = UnitsContainer(
                        {f"scaled-dimensionless ({self.scaling:.2g})": 1},
                    )
            else:
                units = UnitsContainer(
                    {
                        self._REGISTRY._get_symbol(key): value
                        for key, value in self._units.items()
                    },
                )
            spec = spec.replace("~", "")
        else:
            units = self._units

        return formatting.format_unit(units, spec, registry=self._REGISTRY)

    Unit.__format__ = __format__

    if globals().get("U_", None) is None:
        # filename = resource_filename(PKG, 'spectrochempy.txt')
        U_ = UnitRegistry(on_redefinition="ignore")  # filename)

        U_.define(
            "__wrapped__ = 1",
        )  # <- hack to avoid an error with pytest (doctest activated)
        U_.define("@alias point = count")
        U_.define("transmittance = 1. / 100.")
        U_.define("absolute_transmittance = 1.")
        U_.define("absorbance = 1. = a.u.")
        U_.define("Kubelka_Munk = 1. = K.M.")
        U_.define("ppm = 1. = ppm")

        if pint_version < 20:
            U_.define(UnitDefinition("percent", "pct", (), ScaleConverter(1 / 100.0)))
            U_.define(
                UnitDefinition(
                    "weight_percent",
                    "wt_pct",
                    (),
                    ScaleConverter(1 / 100.0),
                ),
            )
        else:
            U_.define(
                UnitDefinition(
                    "percent",
                    "pct",
                    (),
                    ScaleConverter(1 / 100.0),
                    UnitsContainer(),
                ),
            )
            U_.define(
                UnitDefinition(
                    "weight_percent",
                    "wt_pct",
                    (),
                    ScaleConverter(1 / 100.0),
                    UnitsContainer(),
                ),
            )

        U_.default_format = "~P"
        Q_ = U_.Quantity
        Q_.default_format = "~P"

        set_application_registry(U_)
        del UnitRegistry  # to avoid importing it

    else:
        warnings.warn(
            "Unit registry was already set up. Bypassed the new loading",
            stacklevel=2,
        )

    U_.enable_contexts("spectroscopy", "boltzmann", "chemistry")

    # set alias for units and uncertainties
    # --------------------------------------------------------------------------------------
    ur = U_
    Quantity = Q_

    # utilities

    # Context for NMR
    # --------------------------------------------------------------------------------------
    def set_nmr_context(larmor):
        """
        Set a NMR context relative to the given Larmor frequency.

        Parameters
        ----------
        larmor : `Quantity` or `float`
            The Larmor frequency of the current nucleus.
            If it is not a quantity it is assumed to be given in MHz.

        Examples
        --------
        First we set the NMR context,

        >>> from spectrochempy.core.units import ur, set_nmr_context
        >>>
        >>> set_nmr_context(104.3 * ur.MHz)

        then, we can use the context as follow

        >>> fhz = 10000 * ur.Hz
        >>> with ur.context('nmr'):
        ...     fppm = fhz.to('ppm')
        >>> print("{:~.3f}".format(fppm))
        95.877 ppm

        or in the opposite direction

        >>> with ur.context('nmr'):
        ...     fhz = fppm.to('kHz')
        >>> print("{:~.3f}".format(fhz))
        10.000 kHz

        Now we update the context :

        >>> with ur.context('nmr', larmor=100. * ur.MHz):
        ...     fppm = fhz.to('ppm')
        >>> print("{:~.3f}".format(fppm))
        100.000 ppm

        >>> set_nmr_context(75 * ur.MHz)
        >>> fhz = 10000 * ur.Hz
        >>> with ur.context('nmr'):
        ...     fppm = fhz.to('ppm')
        >>> print("{:~.3f}".format(fppm))
        133.333 ppm

        """
        if not isinstance(larmor, U_.Quantity):
            larmor = larmor * U_.MHz

        if "nmr" not in list(ur._contexts.keys()):
            c = Context("nmr", defaults={"larmor": larmor})

            c.add_transformation(
                "[]",
                "[frequency]",
                lambda ur, x, **kwargs: x * kwargs.get("larmor") / 1.0e6,
            )
            c.add_transformation(
                "[frequency]",
                "[]",
                lambda U_, x, **kwargs: x * 1.0e6 / kwargs.get("larmor"),
            )
            U_.add_context(c)

        else:
            c = U_._contexts["nmr"]
            c.defaults["larmor"] = larmor

else:  # pint version >= 24
    from functools import wraps

    from pint import Context
    from pint import DimensionalityError
    from pint import Unit
    from pint import UnitRegistry
    from pint import set_application_registry

    # utilities
    from pint.delegates.formatter._compound_unit_helpers import localize_per
    from pint.delegates.formatter._compound_unit_helpers import prepare_compount_unit
    from pint.delegates.formatter._format_helpers import formatter
    from pint.delegates.formatter._format_helpers import pretty_fmt_exponent

    # formatters to be  subclassed
    from pint.delegates.formatter.full import FullFormatter
    from pint.delegates.formatter.html import HTMLFormatter
    from pint.delegates.formatter.latex import LatexFormatter
    from pint.delegates.formatter.latex import latex_escape
    from pint.delegates.formatter.plain import CompactFormatter
    from pint.delegates.formatter.plain import DefaultFormatter
    from pint.delegates.formatter.plain import PrettyFormatter
    from pint.facets.plain import ScaleConverter
    from pint.facets.plain import UnitDefinition
    from pint.util import UnitsContainer

    ####################################################################################
    # SpectroChemPy specific formatters
    # ##################################################################################
    class ScpDefaultFormatter(DefaultFormatter):
        """Subclasses the DefaultFormatter to provide a specific formatting for SpectroChemPy."""

        def format_unit(self, unit, uspec, sort_func, **babel_kwds) -> str:
            numerator, denominator = prepare_compount_unit(
                unit,
                uspec,
                sort_func=sort_func,
                **babel_kwds,
                registry=self._registry,
            )

            return formatter(
                numerator,
                denominator,
                as_ratio=False,
                single_denominator=False,
                product_fmt=" ",
                division_fmt="/",
                power_fmt="{}^{}",
                parentheses_fmt=r"({})",
            )

    class ScpCompactFormatter(CompactFormatter):
        """Subclasses the CompactFormatter to provide a specific formatting for SpectroChemPy."""

        def format_unit(self, unit, uspec, sort_func, **babel_kwds) -> str:
            numerator, denominator = prepare_compount_unit(
                unit,
                uspec,
                sort_func=sort_func,
                **babel_kwds,
                registry=self._registry,
            )

            return formatter(
                numerator,
                denominator,
                as_ratio=False,
                single_denominator=False,
                product_fmt="*",
                division_fmt="/",
                power_fmt="{}**{}",
                parentheses_fmt=r"({})",
            )

    class ScpPrettyFormatter(PrettyFormatter):
        """Subclasses the PretyFormatter to provide a specific formatting for SpectroChemPy."""

        def format_unit(self, unit, uspec, sort_func, **babel_kwds) -> str:
            numerator, denominator = prepare_compount_unit(
                unit,
                uspec,
                sort_func=sort_func,
                **babel_kwds,
                registry=self._registry,
            )

            return formatter(
                numerator,
                denominator,
                as_ratio=False,
                single_denominator=False,
                product_fmt="⋅",
                division_fmt="/",
                power_fmt="{}{}",
                parentheses_fmt=r"({})",
                exp_call=pretty_fmt_exponent,
            )

    class ScpHTMLFormatter(HTMLFormatter):
        """Subclasses the HTMLFormatter to provide a specific formatting for SpectroChemPy."""

        def format_unit(self, unit, uspec, sort_func, **babel_kwds) -> str:
            numerator, denominator = prepare_compount_unit(
                unit,
                uspec,
                sort_func=sort_func,
                **babel_kwds,
                registry=self._registry,
            )

            if babel_kwds.get("locale"):
                length = babel_kwds.get("length") or (
                    "short" if "~" in uspec else "long"
                )
                division_fmt = localize_per(length, babel_kwds.get("locale"), "{}/{}")
            else:
                division_fmt = "{}/{}"

            return formatter(
                numerator,
                denominator,
                as_ratio=False,
                single_denominator=True,
                product_fmt=r"⋅",
                division_fmt=division_fmt,
                power_fmt=r"{}<sup>{}</sup>",
                parentheses_fmt=r"({})",
            )

    class ScpLatexFormatter(LatexFormatter):
        """Subclasses the LatexFormatter to provide a specific formatting for SpectroChemPy."""

        def format_unit(self, unit, uspec, sort_func, **babel_kwds) -> str:
            numerator, denominator = prepare_compount_unit(
                unit,
                uspec,
                sort_func=sort_func,
                **babel_kwds,
                registry=self._registry,
            )

            numerator = ((rf"\mathrm{{{latex_escape(u)}}}", p) for u, p in numerator)
            denominator = (
                (rf"\mathrm{{{latex_escape(u)}}}", p) for u, p in denominator
            )

            formatted = formatter(
                numerator,
                denominator,
                as_ratio=False,
                single_denominator=True,
                product_fmt=r" \cdot ",
                division_fmt=r"\frac[{}][{}]",
                power_fmt="{}^[{}]",
                parentheses_fmt=r"\left({}\right)",
            )

            return formatted.replace("[", "{").replace("]", "}")

    class ScpFullFormatter(FullFormatter):
        """Subclasses the Formatter to provide a specific formatting for SpectroChemPy."""

        default_format: str = "~P"

        def __init__(self, registry):
            super().__init__(registry)

            self._formatters = {}
            self._formatters["D"] = ScpDefaultFormatter(registry)
            self._formatters["C"] = ScpCompactFormatter(registry)
            self._formatters["P"] = ScpPrettyFormatter(registry)
            self._formatters["H"] = ScpHTMLFormatter(registry)
            self._formatters["L"] = ScpLatexFormatter(registry)

    ####################################################################################
    # Spectrochempy UnitRegistry
    ####################################################################################

    if globals().get("ur", None) is None:
        ur = UnitRegistry(on_redefinition="ignore")

        ur = UnitRegistry()
        ur.formatter = ScpFullFormatter(ur)
        ur.formatter._registry = ur

        Quantity = ur.Quantity

        ur.define(
            "__wrapped__ = 1",
        )  # <- hack to avoid an error with pytest (doctest activated)
        ur.define("@alias point = count")
        ur.define("transmittance = 1. / 100. = %")
        ur.define("absolute_transmittance = 1.")
        ur.define("absorbance = 1. = a.u.")
        ur.define("Kubelka_Munk = 1. = K.M.")
        ur.define("ppm = 1. = ppm")

        set_application_registry(ur)
        del UnitRegistry  # to avoid importing it

    else:
        warnings.warn(
            "Unit registry was already set up. Bypassed the new loading",
            stacklevel=2,
        )

    ur.enable_contexts("spectroscopy", "boltzmann", "chemistry")

    ###################################################################################
    # Context for NMR
    ###################################################################################
    def set_nmr_context(larmor):
        """
        Set a NMR context relative to the given Larmor frequency.

        Parameters
        ----------
        larmor : `Quantity` or `float`
            The Larmor frequency of the current nucleus.
            If it is not a quantity it is assumed to be given in MHz.

        Examples
        --------
        First we set the NMR context,

        >>> from spectrochempy.core.units import ur, set_nmr_context
        >>>
        >>> set_nmr_context(104.3 * ur.MHz)

        then, we can use the context as follow

        >>> fhz = 10000 * ur.Hz
        >>> with ur.context('nmr'):
        ...     fppm = fhz.to('ppm')
        >>> print("{:~.3f}".format(fppm))
        95.877 ppm

        or in the opposite direction

        >>> with ur.context('nmr'):
        ...     fhz = fppm.to('kHz')
        >>> print("{:~.3f}".format(fhz))
        10.000 kHz

        Now we update the context :

        >>> with ur.context('nmr', larmor=100. * ur.MHz):
        ...     fppm = fhz.to('ppm')
        >>> print("{:~.3f}".format(fppm))
        100.000 ppm

        >>> set_nmr_context(75 * ur.MHz)
        >>> fhz = 10000 * ur.Hz
        >>> with ur.context('nmr'):
        ...     fppm = fhz.to('ppm')
        >>> print("{:~.3f}".format(fppm))
        133.333 ppm

        """
        if not isinstance(larmor, ur.Quantity):
            larmor = larmor * ur.MHz

        if "nmr" not in list(ur._contexts.keys()):
            c = Context("nmr", defaults={"larmor": larmor})

            c.add_transformation(
                "[]",
                "[frequency]",
                lambda ur, x, **kwargs: x * kwargs.get("larmor") / 1.0e6,
            )
            c.add_transformation(
                "[frequency]",
                "[]",
                lambda U_, x, **kwargs: x * 1.0e6 / kwargs.get("larmor"),
            )
            ur.add_context(c)

        else:
            c = ur._contexts["nmr"]
            c.defaults["larmor"] = larmor


########################################################################################
# utilities
########################################################################################


def remove_args_units(func):
    """Remove units of arguments of a function."""

    def _remove_units(val):
        if isinstance(val, Quantity):
            val = val.m
        elif isinstance(val, list | tuple):
            val = type(val)([_remove_units(v) for v in val])
        return val

    @wraps(func)
    def new_func(*args, **kwargs):
        args = tuple([_remove_units(arg) for arg in args])
        kwargs = {key: _remove_units(val) for key, val in kwargs.items()}
        return func(*args, **kwargs)

    return new_func
