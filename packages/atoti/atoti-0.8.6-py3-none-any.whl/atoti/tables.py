from collections.abc import Iterable, Mapping
from typing import Any

from atoti_core import (
    ActiveViamClient,
    DelegateMutableMapping,
    Plugin,
    ReprJson,
    ReprJsonable,
    TableIdentifier,
)
from typing_extensions import override

from ._java_api import JavaApi
from .table import Table, _LoadKafka, _LoadSql


class Tables(DelegateMutableMapping[str, Table], ReprJsonable):
    r"""Manage the local :class:`~atoti.Table`\ s of a :class:`~atoti.Session`."""

    def __init__(
        self,
        *,
        client: ActiveViamClient,
        java_api: JavaApi,
        load_kafka: _LoadKafka,
        load_sql: _LoadSql,
        plugins: Mapping[str, Plugin],
    ):
        self._client = client
        self._java_api = java_api
        self._load_kafka = load_kafka
        self._load_sql = load_sql
        self._plugins = plugins

    @override
    def _repr_json_(self) -> ReprJson:
        return (
            dict(
                sorted(
                    {
                        table.name: table._repr_json_()[0] for table in self.values()
                    }.items()
                )
            ),
            {"expanded": False, "root": "Tables"},
        )

    @override
    def _update(
        self,
        other: Mapping[str, Table],
        /,
    ) -> None:
        raise AssertionError(
            "Use `Session.create_table()` or other methods such as `Session.read_pandas()` to create a table."
        )

    @override
    def _get_underlying(self) -> dict[str, Table]:
        return {
            table_name: self._unchecked_getitem(table_name)
            for table_name in self._java_api.get_table_names()
        }

    @override
    def __getitem__(self, key: str, /) -> Table:
        if key not in self._java_api.get_table_names():
            raise KeyError(key)
        return self._unchecked_getitem(key)

    def _unchecked_getitem(self, key: str, /) -> Table:
        return Table(
            TableIdentifier(key),
            client=self._client,
            java_api=self._java_api,
            load_kafka=self._load_kafka,
            load_sql=self._load_sql,
            plugins=self._plugins,
        )

    @override
    def _delete_keys(self, keys: Iterable[str], /) -> None:
        for key in keys or self.keys():
            self._java_api.delete_table(TableIdentifier(key))

    @property
    def schema(self) -> Any:
        """Schema of the tables, as an SVG image in IPython, as a path to the image otherwise.

        Note:
            This requires `Graphviz <https://www.graphviz.org>`__ >=6.0 to be installed.

        """
        return self._java_api.generate_schema_graph()
