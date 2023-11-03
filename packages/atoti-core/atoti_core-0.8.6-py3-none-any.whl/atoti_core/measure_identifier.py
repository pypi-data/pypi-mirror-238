from dataclasses import dataclass

from typing_extensions import override

from .identifier import Identifier


@dataclass(frozen=True)
class MeasureIdentifier(Identifier):  # pylint: disable=keyword-only-dataclass
    measure_name: str

    def __post_init__(self) -> None:
        if "," in self.measure_name:
            raise ValueError(
                f"Invalid measure name `{self.measure_name}`: `,` is not allowed."
            )
        if self.measure_name != self.measure_name.strip():
            raise ValueError(
                f"Invalid measure name `{self.measure_name}`: leading or trailing whitespaces are not allowed."
            )

    @override
    def __repr__(self) -> str:
        return f"""m["{self.measure_name}"]"""
