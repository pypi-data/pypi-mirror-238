from __future__ import annotations

from atoti_core import BaseLevel, ColumnIdentifier, DataType, LevelIdentifier, ReprJson
from typing_extensions import override

from ._java_api import JavaApi
from .order._order import Order


class Level(BaseLevel):
    """Level of a :class:`~atoti.Hierarchy`.

    A level is a sub category of a hierarchy.
    Levels have a specific order with a parent-child relationship.

    In a :guilabel:`Pivot Table`, a single-level hierarchy will be displayed as a flat attribute while a multi-level hierarchy will display the first level and allow users to expand each member against the next level and display sub totals.

    For example, a :guilabel:`Geography` hierarchy can have a :guilabel:`Continent` as the top level where :guilabel:`Continent` expands to :guilabel:`Country` which in turn expands to the leaf level: :guilabel:`City`.
    """

    def __init__(
        self,
        identifier: LevelIdentifier,
        /,
        *,
        column_identifier: ColumnIdentifier,
        cube_name: str,
        data_type: DataType,
        java_api: JavaApi,
    ) -> None:
        super().__init__(identifier)

        self._column_identifier = column_identifier
        self._cube_name = cube_name
        self._data_type: DataType = data_type
        self._java_api = java_api

    @property
    def data_type(self) -> DataType:
        """Type of the level members."""
        return self._data_type

    @property
    def order(self) -> Order:
        """Order in which to sort the level's members.

        Defaults to ascending :class:`atoti.NaturalOrder`.
        """
        return self._java_api.get_level_order(
            self._identifier, cube_name=self._cube_name
        )

    @order.setter
    def order(self, value: Order) -> None:
        self._java_api.update_level_order(
            self._identifier,
            value,
            cube_name=self._cube_name,
        )
        self._java_api.refresh()

    @override
    def _repr_json_(self) -> ReprJson:
        data = {
            "dimension": self.dimension,
            "hierarchy": self.hierarchy,
            "type": str(self.data_type),
            "order": self.order._key,
        }
        return data, {"expanded": True, "root": self.name}
