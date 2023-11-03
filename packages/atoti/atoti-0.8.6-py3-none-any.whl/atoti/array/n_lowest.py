from __future__ import annotations

from .._measure_convertible import MeasureConvertible, NonConstantMeasureConvertible
from .._measure_description import MeasureDescription, convert_to_measure_description
from .._measures.calculated_measure import CalculatedMeasure, Operator
from ._utils import check_array_type, validate_n_argument


def n_lowest(
    measure: NonConstantMeasureConvertible, /, n: MeasureConvertible
) -> MeasureDescription:
    """Return an array measure containing the *n* lowest elements of the passed array measure.

    The values in the returned array are not sorted, use :func:`atoti.array.sort` to sort them.

    Example:
        >>> pnl_table = session.read_csv(
        ...     f"{RESOURCES}/pnl.csv",
        ...     array_separator=";",
        ...     keys=["Continent", "Country"],
        ...     table_name="PnL",
        ... )
        >>> cube = session.create_cube(pnl_table)
        >>> l, m = cube.levels, cube.measures
        >>> m["Bottom 5"] = tt.array.n_lowest(m["PnL.SUM"], n=5)
        >>> cube.query(m["PnL.SUM"], m["Bottom 5"])
                                  PnL.SUM                       Bottom 5
        0  doubleVector[10]{-20.163, ...}  doubleVector[5]{-20.163, ...}

    """
    validate_n_argument(n)
    check_array_type(measure)
    return CalculatedMeasure(
        Operator(
            "n_lowest", [convert_to_measure_description(arg) for arg in [measure, n]]
        )
    )
