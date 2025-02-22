from typing import Annotated

from fastapi import Depends, Query


def pagination_details(
    *, offset: int, limit: int, counts: int
) -> tuple[int, int, int | None, int | None]:
    """Calculate the pagination details.

    Args:
        offset (int): Offset value.
        limit (int): Limit value.
        counts (int): Total number of counts.

    Returns:
        Tuple: Tuple of number of pages, current page, next page, and previous page.
    """
    number_of_pages = (counts + limit - 1) // limit
    current_page = (offset // limit) + 1
    next_page = current_page + 1 if current_page < number_of_pages else None
    previous_page = current_page - 1 if current_page > 1 else None
    return number_of_pages, current_page, next_page, previous_page


async def pager_params(
    skip: int = Query(
        default=0,
        ge=0,
        title="Skip",
        description="Number of items to be skipped",
        examples=[0],
    ),
    limit: int = Query(
        default=100,
        ge=1,
        le=1000,
        title="Limit",
        description="Limit should be between 1 and 1000",
        examples=[100],
    ),
) -> dict[str, int]:
    """Get the pagination parameters.

    Args:
        skip (int, optional): Skip value. Defaults to Query(default=0, ge=0,
                              title="Skip",
                              description="Number of items to be skipped",
                              example=0,).
        limit (int, optional): Limit value. Defaults to Query(default=100,
                               ge=1, le=1000, title="Limit",
                               description="Limit should be between 1 and 1000",
                               example=100, ).

    Returns:
        Dict[str, int]: Dictionary of skip and limit values.
    """
    return {"skip": skip, "limit": limit}


pager_params_dependency = Annotated[dict[str, int], Depends(pager_params)]
