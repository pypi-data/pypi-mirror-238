from collections.abc import Mapping
from typing import Any, Union

IPythonKeyCompletions = list[Union[str, tuple[str, str]]]


def get_ipython_key_completions_for_mapping(
    mapping: Union[Mapping[str, Any], Mapping[tuple[str, ...], Any]]
) -> IPythonKeyCompletions:
    """Return IPython key completions for mapping."""
    return sorted({key if isinstance(key, str) else key[-1] for key in mapping})
