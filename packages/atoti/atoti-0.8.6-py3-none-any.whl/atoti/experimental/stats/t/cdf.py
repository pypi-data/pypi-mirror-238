from __future__ import annotations

from ...._measure_convertible import NonConstantMeasureConvertible
from ...._measure_description import MeasureDescription, convert_to_measure_description
from ...._measures.calculated_measure import CalculatedMeasure, Operator
from .._utils import NumericMeasureConvertible, ensure_strictly_positive


def cdf(
    point: NonConstantMeasureConvertible,
    /,
    *,
    degrees_of_freedom: NumericMeasureConvertible,
) -> MeasureDescription:
    """Cumulative distribution function for a Student's t distribution.

    Args:
        point: The point where the function is evaluated.
        degrees_of_freedom: The number of degrees of freedom.
            Must be positive.

    See Also:
        `The Student's t Wikipedia page <https://en.wikipedia.org/wiki/Student%27s_t-distribution>`__

    """
    ensure_strictly_positive(degrees_of_freedom, "degrees_of_freedom")
    return CalculatedMeasure(
        Operator(
            "student_cumulative_probability",
            [
                convert_to_measure_description(arg)
                for arg in [point, degrees_of_freedom]
            ],
        )
    )
