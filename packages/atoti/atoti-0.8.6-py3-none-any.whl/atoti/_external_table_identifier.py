from dataclasses import dataclass

from atoti_core import Identifier
from typing_extensions import override


@dataclass(frozen=True)
class ExternalTableIdentifier(Identifier):  # pylint: disable=keyword-only-dataclass
    database_name: str
    schema_name: str
    table_name: str

    @override
    def __repr__(self) -> str:
        return f"""t[{self.database_name, self.schema_name, self.table_name}]"""
