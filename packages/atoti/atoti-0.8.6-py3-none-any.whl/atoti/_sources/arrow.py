from __future__ import annotations

from atoti_core import TableIdentifier
from typing_extensions import override

from .._path_utils import to_absolute_path
from .data_source import DataSource


class ArrowDataSource(DataSource):
    @property
    @override
    def key(self) -> str:
        return "ARROW"

    def load_arrow_into_table(
        self,
        identifier: TableIdentifier,
        path: str,
        /,
        *,
        scenario_name: str,
    ) -> None:
        self.load_data_into_table(
            identifier,
            {
                "absolutePath": to_absolute_path(path),
            },
            scenario_name=scenario_name,
        )
