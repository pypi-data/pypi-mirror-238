from __future__ import annotations

from .._measure_convertible import MeasureConvertible, NonConstantMeasureConvertible
from .._measure_description import MeasureDescription, convert_to_measure_description
from .._measures.calculated_measure import CalculatedMeasure, Operator
from ._utils import check_array_type, validate_n_argument


def nth_lowest(
    measure: NonConstantMeasureConvertible, /, n: MeasureConvertible
) -> MeasureDescription:
    """Return a measure equal to the *n*-th lowest element of the passed array measure.

    Example:
        >>> pnl_table = session.read_csv(
        ...     f"{RESOURCES}/pnl.csv",
        ...     array_separator=";",
        ...     keys=["Continent", "Country"],
        ...     table_name="PnL",
        ... )
        >>> cube = session.create_cube(pnl_table)
        >>> l, m = cube.levels, cube.measures
        >>> m["3rd lowest"] = tt.array.nth_lowest(m["PnL.SUM"], n=3)
        >>> cube.query(m["PnL.SUM"], m["3rd lowest"])
                                  PnL.SUM 3rd lowest
        0  doubleVector[10]{-20.163, ...}     -57.51

    """
    validate_n_argument(n)
    check_array_type(measure)
    return CalculatedMeasure(
        Operator(
            "nth_lowest", [convert_to_measure_description(arg) for arg in [measure, n]]
        )
    )
