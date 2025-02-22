from sqlalchemy import func
from sqlmodel import select
from sqlmodel.sql._expression_select_cls import SelectOfScalar

from src.db.models.admin_user import AdminUser
from src.db.models.author import Author
from src.db.models.book import Book


def get_admin_user_stmt(user_id: str) -> SelectOfScalar[AdminUser]:
    """This function returns a select statement to get the admin user.

    Args:
        user_id (str): user_id

    Returns:
        SelectOfScalar[AdminUser]: Select statement for admin_user.
    """
    stmt = select(AdminUser).where(AdminUser.user_id == user_id)
    return stmt


def get_author_stmt(author_id: int) -> SelectOfScalar[Author]:
    """This function returns a select statement to get the Author.

    Args:
        author_id (int): The author id

    Returns:
        SelectOfScalar[Author]: Select statement for author.
    """
    stmt = select(Author).where(Author.id == author_id)
    return stmt


def get_author_count_stmt() -> SelectOfScalar[int]:
    """This function returns a select statement to get the total number of authors.

    Returns:
        SelectOfScalar[int]: Select statement for the count of author.
    """
    stmt = select(func.count().label("author_count")).select_from(Author)
    return stmt


def get_authors_stmt_with_limit_and_offset(*, offset: int, limit: int) -> SelectOfScalar[Author]:
    """This function returns a select statement to get all authors with pagination.

    Args:
        offset (int): Offset value.
        limit (int): Limit value.

    Returns:
        SelectOfScalar[Author]: Select statement for all authors.
    """
    stmt = select(Author).limit(limit).offset(offset).order_by(Author.id.asc())  # type: ignore
    return stmt


def get_book_stmt(book_id: int) -> SelectOfScalar[Book]:
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
