from __future__ import annotations

from collections.abc import Mapping

from atoti_core import BaseHierarchy, HierarchyIdentifier, LevelIdentifier
from typing_extensions import override

from ._java_api import JavaApi
from ._level_arguments import LevelArguments
from .level import Level


class Hierarchy(BaseHierarchy[Level]):
    """Hierarchy of a :class:`~atoti.Cube`.

    A hierarchy is a sub category of a :attr:`~dimension` and represents a precise type of data.

    For example, :guilabel:`Quarter` or :guilabel:`Week` could be hierarchies in the :guilabel:`Time` dimension.

    See Also:
        :class:`~atoti.hierarchies.Hierarchies` to define one.
    """

    def __init__(
        self,
        identifier: HierarchyIdentifier,
        /,
        *,
        cube_name: str,
        java_api: JavaApi,
        levels_arguments: Mapping[str, LevelArguments],
        slicing: bool,
        visible: bool,
        virtual: bool,
    ) -> None:
        super().__init__(identifier)

        self._cube_name = cube_name
        self._java_api = java_api
        self._slicing = slicing
        self._visible = visible
        self._virtual = virtual

        self._levels: Mapping[str, Level] = {
            level_name: Level(
                LevelIdentifier(identifier, level_name),
                column_identifier=level_arguments[1],
                cube_name=self._cube_name,
                data_type=level_arguments[2],
                java_api=self._java_api,
            )
            for level_name, level_arguments in levels_arguments.items()
        }

    @property
    @override
    def levels(self) -> Mapping[str, Level]:
        return self._levels

    @property
    def virtual(self) -> bool:
        """Whether the hierarchy is virtual or not.

        A virtual hierarchy is a lightweight hierarchy which does not store in memory the list of its members.
        It is useful for hierarchies with large cardinality.
        """
        return self._virtual

    @virtual.setter
    def virtual(self, virtual: bool, /) -> None:
        self._java_api.update_hierarchy_virtual(
            self._identifier,
            virtual,
            cube_name=self._cube_name,
        )
        self._java_api.refresh()
        self._virtual = virtual

    # mypy does not detect the decorator just below.
    @property  # type: ignore[explicit-override]
    @override
    def dimension(self) -> str:
        """Name of the dimension of the hierarchy.

        Note:
            If all the hierarchies in a dimension have their deepest level of type ``TIME``, the dimension's type will be set to ``TIME`` too.
            This can be useful for some clients such as Excel which rely on the dimension's type to be ``TIME`` to decide whether to display date filters.
        """
        return self._identifier.dimension_name

    @dimension.setter
    def dimension(self, value: str) -> None:
        self._java_api.update_hierarchy_dimension(
            self._identifier,
            value,
            cube_name=self._cube_name,
        )
        self._java_api.refresh()
        self._BaseHierarchy__identifier = HierarchyIdentifier(value, self.name)

    # mypy does not detect the decorator just below.
    @property  # type: ignore[explicit-override]
    @override
    def slicing(self) -> bool:
        return self._slicing

    @slicing.setter
    def slicing(self, value: bool) -> None:
        """Slicing setter."""
        self._java_api.update_hierarchy_slicing(
            self._identifier,
            value,
            cube_name=self._cube_name,
        )
        self._java_api.refresh()
        self._slicing = value

    @property
    def visible(self) -> bool:
        """Whether the hierarchy is visible or not."""
        return self._visible

    @visible.setter
    def visible(self, value: bool) -> None:
        """Visibility setter."""
        self._java_api.set_hierarchy_visibility(
            self._identifier, value, cube_name=self._cube_name
        )
        self._java_api.refresh()
        self._visible = value
