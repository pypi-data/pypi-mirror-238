from collections.abc import Iterator, Mapping
from typing import TypeVar

from typing_extensions import override

from .ipython_key_completions import (
    IPythonKeyCompletions,
    get_ipython_key_completions_for_mapping,
)

_Key = TypeVar("_Key")
_Value = TypeVar("_Value")


class ImmutableMapping(Mapping[_Key, _Value]):
    def __init__(self, data: Mapping[_Key, _Value], /) -> None:
        super().__init__()

        self._data = data

    @override
    def __getitem__(self, key: _Key, /) -> _Value:
        return self._data[key]

    @override
    def __iter__(self) -> Iterator[_Key]:
        return iter(self._data)

    @override
    def __len__(self) -> int:
        return len(self._data)

    @override
    def __repr__(self) -> str:
        return repr(self._data)

    def _ipython_key_completions_(self) -> IPythonKeyCompletions:
        return get_ipython_key_completions_for_mapping(self)  # type: ignore[arg-type] # pyright: ignore[reportGeneralTypeIssues]
