from collections.abc import Iterable
from dataclasses import dataclass
from typing import Literal, Optional

from atoti_core import (
    Condition,
    Constant,
    Identifiable,
    LevelIdentifier,
    MeasureIdentifier,
    identify,
)

_Key = Literal["bitmap", "leaf"]

_Filter = Condition[
    LevelIdentifier, Literal["eq", "isin"], Constant, Optional[Literal["and"]]
]

_Levels = tuple[LevelIdentifier, ...]
_Measures = tuple[MeasureIdentifier, ...]


@dataclass(frozen=True)
class AggregateProvider:
    """An aggregate provider pre-aggregates some table columns up to certain levels.

    If a step of a query uses a subset of the aggregate provider's levels and measures, the provider will speed up the query.

    An aggregate provider uses additional memory to store the intermediate aggregates.
    The more levels and measures are added, the more memory it requires.

    Example:
        >>> df = pd.DataFrame(
        ...     {
        ...         "Seller": ["Seller_1", "Seller_1", "Seller_2", "Seller_2"],
        ...         "ProductId": ["aBk3", "ceJ4", "aBk3", "ceJ4"],
        ...         "Price": [2.5, 49.99, 3.0, 54.99],
        ...     }
        ... )
        >>> table = session.read_pandas(df, table_name="Seller")
        >>> cube = session.create_cube(table)
        >>> l, m = cube.levels, cube.measures
        >>> cube.aggregate_providers.update(
        ...     {
        ...         "Seller provider": tt.AggregateProvider(
        ...             key="bitmap",
        ...             levels=[l["Seller"], l["ProductId"]],
        ...             measures=[m["Price.SUM"]],
        ...             filter=l["ProductId"] == "cdJ4",
        ...             partitioning="hash4(Seller)",
        ...         )
        ...     }
        ... )
    """

    _key: _Key
    _levels: _Levels
    _measures: _Measures
    _filter: Optional[_Filter] = None
    _partitioning: Optional[str] = None

    def __init__(
        self,
        *,
        key: _Key = "leaf",
        levels: Iterable[Identifiable[LevelIdentifier]] = (),
        measures: Iterable[Identifiable[MeasureIdentifier]] = (),
        filter: Optional[_Filter] = None,  # noqa: A002
        partitioning: Optional[str] = None,
    ) -> None:
        """Initialize an aggregate provider.

        Args:
            key: The key of the provider.

                The bitmap is generally faster but also takes more memory.
            levels: The levels to build the provider on.
            measures: The measures to build in the provider on.
            filter: Only compute and provide aggregates matching this condition.

                The passed condition must be an equality test on a level (handled by the provider or not) or a combination of that kind of condition.
            partitioning: The partitioning of the provider.

                Default to the partitioning of the cube's base table.
        """
        object.__setattr__(self, "_key", key)
        level_identifiers: _Levels = tuple(identify(level) for level in levels)
        object.__setattr__(self, "_levels", level_identifiers)
        measure_identifiers: _Measures = tuple(
            identify(measure) for measure in measures
        )
        object.__setattr__(self, "_measures", measure_identifiers)
        object.__setattr__(self, "_filter", filter)
        object.__setattr__(self, "_partitioning", partitioning)
