from typing import Union

from .has_identifier import HasIdentifier, IdentifierT_co


def get_identifier(
    identifiable: Union[HasIdentifier[IdentifierT_co], IdentifierT_co], /
) -> IdentifierT_co:
    return (
        identifiable._identifier
        if isinstance(identifiable, HasIdentifier)
        else identifiable
    )
