from sqlalchemy import Update, func, update
from sqlmodel import select
from sqlmodel.sql._expression_select_cls import SelectOfScalar

from src.db.models.stock import Stock


def get_stock_book_stmt(book_id: int) -> SelectOfScalar[Stock]:
    """This function returns a select statement to get the Stock.

    Args:
        book_id (int): The book_id to get from DB.

    Returns:
        SelectOfScalar[Stock]: Select statement for Stock.
    """
    stmt = select(Stock).where(Stock.book_id == book_id)
    return stmt


def get_stocks_count_stmt() -> SelectOfScalar[int]:
    """This function returns a select statement to get the total number of stocks.

    Returns:
        SelectOfScalar[int]: Select statement for the count of stocks.
    """
    stmt = select(func.count().label("stocks_count")).select_from(Stock)
    return stmt


def get_stocks_stmt_with_limit_and_offset(*, offset: int, limit: int) -> SelectOfScalar[Stock]:
    """This function returns a select statement to get all stocks with pagination.

    Args:
        offset (int): Offset value.
        limit (int): Limit value.

    Returns:
        SelectOfScalar[Stock]: Select statement for all stocks.
    """
    stmt = select(Stock).limit(limit).offset(offset).order_by(Stock.id.asc())  # type: ignore
    return stmt


def get_decrement_stock_quantity_stmt(book_id: int) -> Update:
    """This function return update stock quantity statement.

    Args:
        book_id (int): Stock quantity to be decremented

    Returns:
         Update: Update statement
    """
    stmt = (
        update(Stock)
        .where(Stock.book_id == book_id)  # type: ignore
        .values(stock_quantity=Stock.stock_quantity - 1)
    )
    return stmt


def get_increment_stock_quantity_stmt(book_id: int) -> Update:
    """This function return update stock quantity statement.

    Args:
        book_id (int): Stock quantity to be incremented.

    Returns:
         Update: Update statement
    """
    stmt = (
        update(Stock)
        .where(Stock.book_id == book_id)  # type: ignore
        .values(stock_quantity=Stock.stock_quantity + 1)
    )
    return stmt
