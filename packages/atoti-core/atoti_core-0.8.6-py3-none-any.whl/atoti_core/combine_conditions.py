from collections.abc import Collection
from typing import Literal, TypeVar, Union, overload

from .boolean_operator import BooleanOperator
from .operation import (
    CombinedCondition,
    Condition,
    ConditionCombinationOperatorBound,
    ConditionCombinationOperatorT_co,
    ConditionComparisonOperatorT_co,
    ConditionSubjectT_co,
    ConditionTargetT_co,
)

_BooleanOperatorT = TypeVar("_BooleanOperatorT", bound=BooleanOperator)


def _combine_conditions(
    *conditions: Condition[
        ConditionSubjectT_co,
        ConditionComparisonOperatorT_co,
        ConditionTargetT_co,
        ConditionCombinationOperatorT_co,
    ],
    operator: _BooleanOperatorT,
) -> Condition[
    ConditionSubjectT_co,
    ConditionComparisonOperatorT_co,
    ConditionTargetT_co,
    Union[ConditionCombinationOperatorT_co, _BooleanOperatorT],
]:
    if not conditions:
        raise ValueError("No conditions to combine.")

    iterator = iter(conditions)
    condition = next(iterator)

    if len(conditions) == 1:
        return condition

    return CombinedCondition(
        sub_conditions=(
            condition,
            _combine_conditions(*iterator, operator=operator),
        ),
        operator=operator,
    )


@overload
# If the top level collection has a single element, the operator `or` will not be used, only `and`.
def combine_conditions(
    conditions: tuple[
        Collection[
            Condition[
                ConditionSubjectT_co,
                ConditionComparisonOperatorT_co,
                ConditionTargetT_co,
                ConditionCombinationOperatorT_co,
            ]
        ]
    ],
    /,
) -> Condition[
    ConditionSubjectT_co,
    ConditionComparisonOperatorT_co,
    ConditionTargetT_co,
    Union[ConditionCombinationOperatorT_co, Literal["and"]],
]:
    ...


@overload
# If all the bottom level collections have a single element, the operator `and` will not be used, only `or`.
def combine_conditions(
    conditions: Collection[
        tuple[
            Condition[
                ConditionSubjectT_co,
                ConditionComparisonOperatorT_co,
                ConditionTargetT_co,
                ConditionCombinationOperatorT_co,
            ]
        ]
    ],
    /,
) -> Condition[
    ConditionSubjectT_co,
    ConditionComparisonOperatorT_co,
    ConditionTargetT_co,
    Union[ConditionCombinationOperatorT_co, Literal["or"]],
]:
    ...


@overload
def combine_conditions(
    conditions: Collection[
        Collection[
            Condition[
                ConditionSubjectT_co,
                ConditionComparisonOperatorT_co,
                ConditionTargetT_co,
                ConditionCombinationOperatorBound,
            ]
        ]
    ],
    /,
) -> Condition[
    ConditionSubjectT_co,
    ConditionComparisonOperatorT_co,
    ConditionTargetT_co,
    ConditionCombinationOperatorBound,
]:
    ...


def combine_conditions(
    conditions: Collection[
        Collection[
            Condition[
                ConditionSubjectT_co,
                ConditionComparisonOperatorT_co,
                ConditionTargetT_co,
                ConditionCombinationOperatorBound,
            ]
        ]
    ],
    /,
) -> Condition[
    ConditionSubjectT_co,
    ConditionComparisonOperatorT_co,
    ConditionTargetT_co,
    ConditionCombinationOperatorBound,
]:
    """Take conditions structured in disjunctive normal form and return a single combined condition."""
    return _combine_conditions(
        *(
            _combine_conditions(*conjunct_conditions, operator="and")
            for conjunct_conditions in conditions
        ),
        operator="or",
    )
