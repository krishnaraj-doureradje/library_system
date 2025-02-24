import pytest

from src.helper.pagination import pagination_details


@pytest.mark.parametrize(
    "offset, limit, counts, expected",
    [
        (0, 10, 50, (5, 1, 2, None)),  # First page with 10 items per page
        (20, 10, 50, (5, 3, 4, 2)),  # Third page with 10 items per page
        (40, 10, 50, (5, 5, None, 4)),  # Last page with 10 items per page
        (0, 50, 50, (1, 1, None, None)),  # Single page with all items
        (0, 10, 0, (0, 1, None, None)),  # No items
        (60, 10, 50, (5, 7, None, 6)),  # Offset beyond total items
        (10, 10, 10, (1, 2, None, 1)),  # Exact fit for one page
        (5, 5, 25, (5, 2, 3, 1)),  # Second page with 5 items per page
        (0, 1, 1, (1, 1, None, None)),  # Single item
        (0, 1, 0, (0, 1, None, None)),  # No items with limit 1
    ],
)
def test_pagination_details(
    offset: int,
    limit: int,
    counts: int,
    expected: tuple[int, int, int | None, int | None],
) -> None:
    """Test pagination details."""
    result = pagination_details(offset=offset, limit=limit, counts=counts)
    assert result == expected, f"Expected {expected}, but got {result}"
