from atoti_core import QueryFilter, decombine_condition
from typing_extensions import TypeGuard

from ._gaq_filter import GaqFilter


# Remove once https://activeviam.atlassian.net/browse/PIVOT-6806 is done.
def is_gaq_filter(
    filter: QueryFilter,  # noqa: A002
    /,
) -> TypeGuard[GaqFilter]:
    return all(  # type: ignore[var-annotated]
        condition.operator == "eq"
        for condition in decombine_condition(
            filter, allowed_combination_operators=("and",)
        )[0][0]
    )
