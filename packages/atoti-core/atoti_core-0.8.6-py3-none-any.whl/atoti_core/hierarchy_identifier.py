from dataclasses import dataclass
from functools import cached_property

from typing_extensions import Self, override

from .identifier import Identifier


@dataclass(frozen=True)
class HierarchyIdentifier(Identifier):  # pylint: disable=keyword-only-dataclass
    dimension_name: str
    hierarchy_name: str

    @classmethod
    def from_java_description(cls, java_description: str, /) -> Self:
        hierarchy_name, dimension_name = java_description.split("@")
        return cls(dimension_name, hierarchy_name)

    @cached_property
    def java_description(self) -> str:
        return "@".join(reversed(self.key))

    @cached_property
    def key(self) -> tuple[str, str]:
        return self.dimension_name, self.hierarchy_name

    @override
    def __repr__(self) -> str:
        return f"h[{self.key}]"
