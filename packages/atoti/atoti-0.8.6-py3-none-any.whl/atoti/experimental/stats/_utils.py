from typing import Union

from ..._measure_convertible import NonConstantMeasureConvertible
from ..._measure_description import MeasureDescription

NumericMeasureConvertible = Union[int, float, NonConstantMeasureConvertible]


def ensure_strictly_positive(arg: NumericMeasureConvertible, arg_name: str) -> None:
    if isinstance(arg, (int, float)):
        if arg <= 0:
            raise ValueError(f"{arg_name} must be greater than 0.")
    elif not isinstance(arg, MeasureDescription):
        raise TypeError(f"{arg_name} must be a measure or an number.")
