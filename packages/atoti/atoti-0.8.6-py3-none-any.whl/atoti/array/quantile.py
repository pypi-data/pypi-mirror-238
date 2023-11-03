from __future__ import annotations

from typing import Literal

from atoti_core import doc

from .._docs_utils import QUANTILE_DOC as _QUANTILE_DOC
from .._measure_convertible import MeasureConvertible, NonConstantMeasureConvertible
from .._measure_description import MeasureDescription, convert_to_measure_description
from .._measures.generic_measure import GenericMeasure
from ._utils import (
    QUANTILE_STD_AND_VAR_DOC_KWARGS as _QUANTILE_STD_AND_VAR_DOC_KWARGS,
    check_array_type,
)

_Interpolation = Literal["linear", "higher", "lower", "nearest", "midpoint"]
_Mode = Literal["simple", "centered", "inc", "exc"]


@doc(_QUANTILE_DOC, **_QUANTILE_STD_AND_VAR_DOC_KWARGS)
def quantile(
    measure: NonConstantMeasureConvertible,
    /,
    q: MeasureConvertible,
    *,
    mode: _Mode = "inc",
    interpolation: _Interpolation = "linear",
) -> MeasureDescription:
    if isinstance(q, float) and (q < 0 or q > 1):
        raise ValueError("Quantile must be between 0 and 1.")
    check_array_type(measure)
    return GenericMeasure(
        "CALCULATED_QUANTILE",
        mode,
        interpolation,
        [convert_to_measure_description(arg) for arg in [measure, q]],
    )
