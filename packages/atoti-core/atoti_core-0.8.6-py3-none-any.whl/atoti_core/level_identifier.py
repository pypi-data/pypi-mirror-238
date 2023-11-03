from dataclasses import dataclass
from functools import cached_property

from typing_extensions import Self, override

from .hierarchy_identifier import HierarchyIdentifier
from .identifier import Identifier


@dataclass(frozen=True)
class LevelIdentifier(Identifier):  # pylint: disable=keyword-only-dataclass
    hierarchy_identifier: HierarchyIdentifier
    level_name: str

    @classmethod
    def from_java_description(cls, java_description: str, /) -> Self:
        level_name, hierarchy_name, dimension_name = java_description.split("@")
        return cls(HierarchyIdentifier(dimension_name, hierarchy_name), level_name)

    @cached_property
    def java_description(self) -> str:
        return "@".join(reversed(self.key))

    @cached_property
    def key(self) -> tuple[str, str, str]:
        return *self.hierarchy_identifier.key, self.level_name

    @override
    def __repr__(self) -> str:
        return f"l[{self.key}]"
