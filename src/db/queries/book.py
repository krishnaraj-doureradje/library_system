from sqlalchemy import Delete, delete, func
from sqlmodel import select
from sqlmodel.sql._expression_select_cls import SelectOfScalar

from src.db.models.book import Book


def get_book_from_id_stmt(book_id: int) -> SelectOfScalar[Book]:
    """This function returns a select statement to get the Book.

    Args:
        book_id (int): The Book id

    Returns:
        SelectOfScalar[Book]: Select statement for book.
    """
    stmt = select(Book).where(Book.id == book_id)
    return stmt


def get_book_count_stmt() -> SelectOfScalar[int]:
    """This function returns a select statement to get the total number of books.

    Returns:
        SelectOfScalar[int]: Select statement for the count of author.
    """
    stmt = select(func.count().label("book_count")).select_from(Book)
    return stmt


def get_books_stmt_with_limit_and_offset(*, offset: int, limit: int) -> SelectOfScalar[Book]:
    """This function returns a select statement to get all books with pagination.

    Args:
        offset (int): Offset value.
        limit (int): Limit value.

    Returns:
        SelectOfScalar[Book]: Select statement for all books.
    """
    stmt = select(Book).limit(limit).offset(offset).order_by(Book.id.asc())  # type: ignore
    return stmt


def delete_book_from_id_stmt(book_id: int) -> Delete:
    """This function return delete book statement

    Args:
        book_id (int): Book id to be deleted

    Returns:
         Delete: Delete statement
    """
    stmt = delete(Book).where(Book.id == book_id)  # type: ignore
    return stmt


def delete_books_from_author_id_stmt(author_id: int) -> Delete:
    """This function return delete book statement by using author_id.

    Args:
        author_id (int): Author id to be deleted

    Returns:
         Delete: Delete statement
    """
    stmt = delete(Book).where(Book.author_id == author_id)  # type: ignore
    return stmt
