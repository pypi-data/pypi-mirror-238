from __future__ import annotations

from typing import Literal, Optional, Union

from .constant import Constant
from .hierarchy_identifier import HierarchyIdentifier
from .level_identifier import LevelIdentifier
from .operation import Condition

QueryFilter = Condition[
    Union[HierarchyIdentifier, LevelIdentifier],
    Literal["eq", "isin", "ne"],
    Constant,
    Optional[Literal["and"]],
]
