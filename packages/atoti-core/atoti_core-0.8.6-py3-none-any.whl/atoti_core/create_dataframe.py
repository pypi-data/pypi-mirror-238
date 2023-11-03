from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Any, Union

import pandas as pd

from .convert_series import convert_series
from .data_type import DataType


@dataclass(frozen=True)
# All the attributes have a different type so they cannot be mixed up.
class DataFrameColumnDescription:  # pylint: disable=keyword-only-dataclass
    name: str
    data_type: DataType
    nullable: bool = False


def create_dataframe(
    rows: Iterable[tuple[Any, ...]],
    columns_or_types: Union[
        # DataFrames can have multiple columns with the same name so a `Mapping` is not enough.
        Iterable[DataFrameColumnDescription],
        Mapping[str, DataType],
    ],
    /,
) -> pd.DataFrame:
    """Return a DataFrame with columns of the given types."""
    columns: Iterable[DataFrameColumnDescription] = (
        [
            DataFrameColumnDescription(
                # Pyright fails to see that the `isinstance` below ensures that `name` is a string.
                name,  # pyright: ignore[reportGeneralTypeIssues]
                data_type,
            )
            for name, data_type in columns_or_types.items()
        ]
        if isinstance(columns_or_types, Mapping)
        else columns_or_types
    )

    dataframe = pd.DataFrame(
        rows,
        columns=[columns.name for columns in columns],
        dtype="object",  # To prevent any preliminary conversion.
    )

    for column in columns:
        converted_series = convert_series(
            dataframe[column.name], data_type=column.data_type, nullable=column.nullable
        )
        dataframe[column.name] = converted_series

    return dataframe
