from __future__ import annotations

from collections.abc import (
    Iterator,
    MutableMapping,
)
from typing import (
    Any,
)

from atoti_core import (
    IPythonKeyCompletions,
    ReprJson,
    ReprJsonable,
    get_ipython_key_completions_for_mapping,
)
from typing_extensions import override

from ._java_api import JavaApi


class CubeContext(MutableMapping[str, str], ReprJsonable):
    """Manage the shared context of a cube."""

    def __init__(self, *, cube_name: str, java_api: JavaApi) -> None:
        super().__init__()

        self._cube_name = cube_name
        self._java_api = java_api

    def _get_values(self) -> dict[str, str]:
        return self._java_api.get_shared_context_values(self._cube_name)

    @override
    def __getitem__(self, key: str, /) -> str:
        return self._get_values()[key]

    @override
    def __setitem__(self, key: str, value: Any, /) -> None:
        self._java_api.set_shared_context_value(
            key,
            str(value),
            cube_name=self._cube_name,
        )
        self._java_api.refresh()

    @override
    def __delitem__(self, key: str, /) -> None:
        raise AssertionError("Cannot delete context value.")

    @override
    def __iter__(self) -> Iterator[str]:
        return iter(self._get_values())

    @override
    def __len__(self) -> int:
        return len(self._get_values())

    def _ipython_key_completions_(self) -> IPythonKeyCompletions:
        return get_ipython_key_completions_for_mapping(self._get_values())

    @override
    def __str__(self) -> str:
        return str(self._get_values())

    @override
    def __repr__(self) -> str:
        return repr(self._get_values())

    @override
    def _repr_json_(self) -> ReprJson:
        return (
            self._get_values(),
            {"expanded": True, "root": "Shared Context Values"},
        )
