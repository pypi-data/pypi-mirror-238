from __future__ import annotations

from .._utils import NumericMeasureConvertible, ensure_strictly_positive


def validate_args(
    numerator_degrees_of_freedom: NumericMeasureConvertible,
    denominator_degrees_of_freedom: NumericMeasureConvertible,
) -> None:
    ensure_strictly_positive(
        numerator_degrees_of_freedom, "numerator_degrees_of_freedom"
    )
    ensure_strictly_positive(
        denominator_degrees_of_freedom, "denominator_degrees_of_freedom"
    )
