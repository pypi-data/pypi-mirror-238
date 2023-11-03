from dataclasses import dataclass

from typing_extensions import override

from .identifier import Identifier
from .table_identifier import TableIdentifier


@dataclass(frozen=True)
class ColumnIdentifier(Identifier):  # pylint: disable=keyword-only-dataclass
    table_identifier: TableIdentifier
    column_name: str

    @property
    def key(self) -> tuple[str, str]:
        return *self.table_identifier.key, self.column_name

    @override
    def __repr__(self) -> str:
        return f"""{self.table_identifier!r}["{self.column_name}"]"""
