from dataclasses import dataclass

from typing_extensions import override

from .identifier import Identifier


@dataclass(frozen=True)
class TableIdentifier(Identifier):  # pylint: disable=keyword-only-dataclass
    table_name: str

    @property
    def key(self) -> tuple[str]:
        return (self.table_name,)

    @override
    def __repr__(self) -> str:
        return f"""t["{self.table_name}"]"""
