from collections.abc import Mapping
from typing import Any

from .immutable_mapping import ImmutableMapping

EMPTY_MAPPING: Mapping[Any, Any] = ImmutableMapping({})
