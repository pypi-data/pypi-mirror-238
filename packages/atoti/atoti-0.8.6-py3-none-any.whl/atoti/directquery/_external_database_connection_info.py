from abc import ABC, abstractmethod
from collections.abc import Mapping
from typing import Generic, Optional

from atoti_core import EMPTY_MAPPING

from .._java_api import JavaApi
from ._external_database_connection import ExternalDatabaseConnectionT
from ._external_table import ExternalTableT_co


class ExternalDatabaseConnectionInfo(
    Generic[ExternalDatabaseConnectionT, ExternalTableT_co], ABC
):
    def __init__(
        self,
        *,
        database_key: str,
        options: Mapping[str, Optional[str]] = EMPTY_MAPPING,
        password: Optional[str] = None,
        url: Optional[str],
    ) -> None:
        super().__init__()

        self._database_key = database_key
        self._options = options
        self._password = password
        self._url = url

    @abstractmethod
    def _get_database_connection(
        self, java_api: JavaApi
    ) -> ExternalDatabaseConnectionT:
        ...
