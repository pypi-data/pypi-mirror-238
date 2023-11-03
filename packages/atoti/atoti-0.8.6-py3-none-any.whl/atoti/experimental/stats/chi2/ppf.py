from __future__ import annotations

from ...._measure_convertible import NonConstantMeasureConvertible
from ...._measure_description import MeasureDescription, convert_to_measure_description
from ...._measures.calculated_measure import CalculatedMeasure, Operator
from .._utils import NumericMeasureConvertible, ensure_strictly_positive


def ppf(
    point: NonConstantMeasureConvertible,
    /,
    *,
    degrees_of_freedom: NumericMeasureConvertible,
) -> MeasureDescription:
    """Percent point function for a chi-square distribution.

    Also called inverse cumulative distribution function.

    Args:
        point: The point where the function is evaluated.
        degrees_of_freedom: The number of degrees of freedom.
            Must be positive.

    See Also:
        `The Chi-square Wikipedia page <https://en.wikipedia.org/wiki/Chi-square_distribution>`__

    """
    ensure_strictly_positive(degrees_of_freedom, "degrees_of_freedom")
    return CalculatedMeasure(
        Operator(
            "chi2_ppf",
            [
                convert_to_measure_description(arg)
                for arg in [point, degrees_of_freedom]
            ],
        )
    )
