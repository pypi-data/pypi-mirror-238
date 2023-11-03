from __future__ import annotations

from collections.abc import Mapping
from functools import reduce
from typing import Optional, Union

from atoti_core import (
    ComparisonCondition,
    Condition,
    Constant,
    HasIdentifier,
    Operation,
)

from .._measure_convertible import (
    MeasureCondition,
    MeasureConvertible,
    MeasureConvertibleIdentifier,
    MeasureOperation,
    NonConstantMeasureConvertible,
)
from .._measure_description import MeasureDescription
from .where import where


def _create_eq_condition(
    *,
    subject: NonConstantMeasureConvertible,
    target: Optional[MeasureConvertible],
) -> MeasureCondition:
    if isinstance(subject, Condition):
        raise TypeError(
            f"Cannot use a `{type(subject).__name__}` as a `{switch.__name__}()` subject."
        )

    condition_target: Optional[
        Union[
            Constant,
            MeasureConvertibleIdentifier,
            MeasureOperation,
        ]
    ] = None

    if target is not None:
        if isinstance(target, Condition):
            raise TypeError(
                f"Cannot use a `{type(target).__name__}` `{switch.__name__}()` target."
            )

        if isinstance(target, HasIdentifier):
            condition_target = target._identifier
        elif isinstance(target, Operation):
            condition_target = target
        else:
            condition_target = Constant(target)

    return ComparisonCondition(
        subject=subject._identifier if isinstance(subject, HasIdentifier) else subject,
        operator="eq",
        target=condition_target,
    )


def switch(
    subject: NonConstantMeasureConvertible,
    cases: Mapping[
        Union[Optional[MeasureConvertible], tuple[Optional[MeasureConvertible], ...]],
        MeasureConvertible,
    ],
    /,
    *,
    default: Optional[MeasureConvertible] = None,
) -> MeasureDescription:
    """Return a measure equal to the value of the first case for which *subject* is equal to the case's key.

    *cases*'s values and *default* must either be all numerical, all boolean or all objects.

    Args:
        subject: The measure or level to compare to *cases*' keys.
        cases: A mapping from keys to compare with *subject* to the values to return if the comparison is ``True``.
        default: The measure to use when none of the *cases* matched.

    Example:
        >>> df = pd.DataFrame(
        ...     columns=["Id", "City", "Value"],
        ...     data=[
        ...         (0, "Paris", 1.0),
        ...         (1, "Paris", 2.0),
        ...         (2, "London", 3.0),
        ...         (3, "London", 4.0),
        ...         (4, "Paris", 5.0),
        ...         (5, "Singapore", 7.0),
        ...         (6, "NYC", 2.0),
        ...     ],
        ... )
        >>> table = session.read_pandas(df, keys=["Id"], table_name="Switch example")
        >>> cube = session.create_cube(table)
        >>> l, m = cube.levels, cube.measures
        >>> m["Continent"] = tt.switch(
        ...     l["City"],
        ...     {
        ...         ("Paris", "London"): "Europe",
        ...         "Singapore": "Asia",
        ...         "NYC": "North America",
        ...     },
        ... )
        >>> cube.query(m["Continent"], levels=[l["City"]])
                       Continent
        City
        London            Europe
        NYC        North America
        Paris             Europe
        Singapore           Asia
        >>> m["Europe & Asia value"] = tt.agg.sum(
        ...     tt.switch(
        ...         m["Continent"], {("Europe", "Asia"): m["Value.SUM"]}, default=0.0
        ...     ),
        ...     scope=tt.OriginScope(l["Id"], l["City"]),
        ... )
        >>> cube.query(m["Europe & Asia value"], levels=[l["City"]])
                  Europe & Asia value
        City
        London                   7.00
        NYC                       .00
        Paris                    8.00
        Singapore                7.00
        >>> cube.query(m["Europe & Asia value"])
          Europe & Asia value
        0               22.00

    See Also:
        :func:`atoti.where`.
    """
    condition_to_measure: dict[
        NonConstantMeasureConvertible,
        MeasureConvertible,
    ] = {}
    for values, measure in cases.items():
        if isinstance(values, tuple):
            condition_to_measure[
                reduce(
                    lambda a, b: a | b,  # pyright: ignore[reportUnknownLambdaType]
                    [
                        _create_eq_condition(subject=subject, target=value)
                        for value in values
                    ],
                )
            ] = measure
        else:
            condition_to_measure[
                _create_eq_condition(subject=subject, target=values)
            ] = measure
    return where(condition_to_measure, default=default)
