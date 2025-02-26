from src.db.engine import db_dependency
from src.db.execution import execute_all_query, fetch_all, fetch_one_or_none, update_statement
from src.db.models.stock import Stock
from src.db.queries.stock import (
    get_add_new_stock_quantity_stmt,
    get_stock_book_stmt,
    get_stocks_count_stmt,
    get_stocks_stmt_with_limit_and_offset,
)
from src.exceptions.app import NotFoundException
from src.helper.pagination import pagination_details
from src.models.http_response_code import HTTPResponseCode
from src.models.stock import StockIn, StockOut, StockQuantityAdd, StocksList


def create_stock_on_db(db_session: db_dependency, stock_in: StockIn) -> StockOut:
    """Create a new stock in the databases

    Args:
        db_session (db_dependency): Database session.
        stock_in (StockIn): Stock details.

    Returns:
        StockOut: Stock details with ID
    """
    new_stock = Stock(**stock_in.model_dump())
    # Refresh the object after commit to get the primary key
    execute_all_query(db_session, [new_stock], is_commit=True, is_refresh_after_commit=True)
    stock_data = new_stock.model_dump()
    book_data = new_stock.book.model_dump()
    return StockOut(
        book_id=stock_data["book_id"],
        stock_quantity=stock_data["stock_quantity"],
        id=stock_data["id"],
        title=book_data["title"],
        category=book_data["category"],
    )


def get_stock_book_from_id(db_session: db_dependency, book_id: int) -> Stock:
    """Get a stock based on the book id.

    Args:
        db_session (db_dependency):  Database session.
        book_id (int): Stock id

    Raises:
        NotFoundException: Raised when the book_id is not found in the database.

    Returns:
        Stock: Stock details
    """
    stock_stmt = get_stock_book_stmt(book_id)
    stock = fetch_one_or_none(db_session, stock_stmt)

    if stock is None:
        raise NotFoundException(
            status_code=HTTPResponseCode.NOT_FOUND,
            message=f"{book_id=} not found in the database",
        )

    return stock


def get_stock_book_out_from_db(db_session: db_dependency, book_id: int) -> StockOut:
    """Get StockOut model response.

    Args:
        db_session (db_dependency): Database session.
        book_id (int): Book id.

    Returns:
        StockOut: Stock details details.
    """
    db_stock = get_stock_book_from_id(db_session, book_id)
    stock_data = db_stock.model_dump()
    book_data = db_stock.book.model_dump()
    return StockOut(
        book_id=stock_data["book_id"],
        stock_quantity=stock_data["stock_quantity"],
        id=stock_data["id"],
        title=book_data["title"],
        category=book_data["category"],
    )


def get_stocks_with_offset_and_limit(
    db_session: db_dependency, *, offset: int, limit: int
) -> StocksList:
    """Get all the stocks with pagination.

    Args:
        db_session (db_dependency): Database session.
        offset (int): Offset value.
        limit (int): Limit value.

    Returns:
        StocksList: List of available stocks.
    """
    stocks_count_stmt = get_stocks_count_stmt()
    stocks_count = fetch_one_or_none(db_session, stocks_count_stmt)  # type: ignore

    # There is nothing to fetch if the stocks_count is None
    if stocks_count is None:
        return StocksList(
            stocks=[],
            number_of_stocks=0,
            number_of_pages=0,
            current_page=0,
            next_page=None,
            previous_page=None,
        )

    stocks_stmt = get_stocks_stmt_with_limit_and_offset(offset=offset, limit=limit)
    stocks: list[StockOut] = []

    for db_stock in fetch_all(db_session, stocks_stmt):
        stock_data = db_stock.model_dump()
        book_data = db_stock.book.model_dump()
        stocks.append(
            StockOut(
                book_id=stock_data["book_id"],
                stock_quantity=stock_data["stock_quantity"],
                id=stock_data["id"],
                title=book_data["title"],
                category=book_data["category"],
            )
        )

    # Calculate the number of pages, current page, next page, and previous page
    number_of_pages, current_page, next_page, previous_page = pagination_details(
        offset=offset, limit=limit, counts=stocks_count
    )

    return StocksList(
        stocks=stocks,
        number_of_stocks=stocks_count,
        number_of_pages=number_of_pages,
        current_page=current_page,
        next_page=next_page,
        previous_page=previous_page,
    )


def add_new_quantity_to_the_existing_stocks_on_db(
    db_session: db_dependency, book_id: int, stock_in: StockQuantityAdd
) -> StockOut:
    """Add new quantity to the existing stocks.

    Args:
        db_session (db_dependency): Database session.
        book_id (int): book id.
        stock_in (StockQuantityAdd): Stock update details.

    Raises:
        NotFoundException: Raised when the stock id is not found in the database.

    Returns:
        StockOut: Updated stock details.
    """
    # Update stock quantity and commit it, then obtain stock details.
    add_new_stock_quantity_stmt = get_add_new_stock_quantity_stmt(book_id, stock_in.stock_quantity)
    update_statement(db_session, add_new_stock_quantity_stmt)

    db_stock = get_stock_book_from_id(db_session, book_id)

    stock_data = db_stock.model_dump()
    book_data = db_stock.book.model_dump()

    stock_out = StockOut(
        book_id=stock_data["book_id"],
        stock_quantity=stock_data["stock_quantity"],
        id=stock_data["id"],
        title=book_data["title"],
        category=book_data["category"],
    )
    # We don't need to refresh the object for the update operation, so we can avoid
    # making a select request to the database.
    execute_all_query(
        db_session,
        [db_stock],  # type: ignore
    )
    return stock_out
