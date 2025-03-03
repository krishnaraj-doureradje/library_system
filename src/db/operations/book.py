from src.db.engine import db_dependency
from src.db.execution import execute_all_query, execute_statement, fetch_all, fetch_one_or_none
from src.db.models.book import Book
from src.db.queries.book import (
    delete_book_from_id_stmt,
    get_book_count_stmt,
    get_book_from_id_stmt,
    get_books_stmt_with_limit_and_offset,
)
from src.exceptions.app import NotFoundException, SqlException
from src.helper.pagination import pagination_details
from src.models.book import BookIn, BookOut, BooksList
from src.models.http_response_code import HTTPResponseCode


def create_book_on_db(db_session: db_dependency, book_in: BookIn) -> BookOut:
    """Create a new book in the databases

    Args:
        db_session (db_dependency): Database session.
        book_in (BookIn): Book details

    Returns:
        BookOut: Book details with ID
    """
    new_book = Book(**book_in.model_dump())
    # Refresh the object after commit to get the primary key
    execute_all_query(db_session, [new_book], is_commit=True, is_refresh_after_commit=True)
    return BookOut(**new_book.model_dump())


def get_book_from_id(db_session: db_dependency, book_id: int) -> Book:
    """Get a book based on the book id.

    Args:
        db_session (db_dependency):  Database session.
        book_id (int): Book id

    Raises:
        NotFoundException: Raised when the book id is not found in the database.

    Returns:
        Book: Book details
    """
    book_stmt = get_book_from_id_stmt(book_id)
    book = fetch_one_or_none(db_session, book_stmt)

    if book is None:
        raise NotFoundException(
            status_code=HTTPResponseCode.NOT_FOUND,
            message=f"{book_id=} not found in the database",
        )

    return book


def get_book_out_from_db(db_session: db_dependency, book_id: int) -> BookOut:
    """Get book based on the book id.

    Args:
        db_session (db_dependency): Database session.
        book_id (int): Book id.

    Returns:
        BookOut: Book details.
    """
    db_book = get_book_from_id(db_session, book_id)
    return BookOut(**db_book.model_dump())


def get_books_with_offset_and_limit(
    db_session: db_dependency, *, offset: int, limit: int
) -> BooksList:
    """Get all books with pagination.

    Args:
        db_session (db_dependency): Database session.
        offset (int): Offset value.
        limit (int): Limit value.

    Returns:
        BooksList: List of books.
    """
    books_count_stmt = get_book_count_stmt()
    books_count = fetch_one_or_none(db_session, books_count_stmt)  # type: ignore

    # There is nothing to fetch if the books_count is None
    if books_count is None:
        return BooksList(
            books=[],
            number_of_books=0,
            number_of_pages=0,
            current_page=0,
            next_page=None,
            previous_page=None,
        )

    books_stmt = get_books_stmt_with_limit_and_offset(offset=offset, limit=limit)
    books = [BookOut(**book.model_dump()) for book in fetch_all(db_session, books_stmt)]

    # Calculate the number of pages, current page, next page, and previous page
    number_of_pages, current_page, next_page, previous_page = pagination_details(
        offset=offset, limit=limit, counts=books_count
    )

    return BooksList(
        books=books,
        number_of_books=books_count,
        number_of_pages=number_of_pages,
        current_page=current_page,
        next_page=next_page,
        previous_page=previous_page,
    )


def update_book_on_db(db_session: db_dependency, book_id: int, book_in: BookIn) -> BookOut:
    """Update a book based on the book id.

    Args:
        db_session (db_dependency): Database session.
        book_id (int): Book id.
        book_in (BookIn): Book details.

    Raises:
        NotFoundException: Raised when the book id is not found in the database.

    Returns:
        BookOut: Updated book details.
    """
    db_book = get_book_from_id(db_session, book_id)

    # Update the Book fields with the new values
    for field, value in book_in.model_dump().items():
        setattr(db_book, field, value)

    book_out = BookOut(**db_book.model_dump())
    # We don't need to refresh the object for the update operation, so we can avoid
    # making a select request to the database.
    execute_all_query(
        db_session,
        [db_book],  # type: ignore
    )
    return book_out


def delete_book_on_db(
    db_session: db_dependency,
    book_id: int,
) -> None:
    """Delete a book based on the book id.

    Args:
        db_session (db_dependency): Database session.
        book_id (int): Book id.
    """
    try:
        db_books = get_book_from_id(db_session, book_id)
    except NotFoundException:
        # Nothing to delete so don't raise exception
        return None

    is_stock_present = any(stock for stock in db_books.stock)
    if is_stock_present:
        raise SqlException(
            status_code=HTTPResponseCode.FORBIDDEN,
            message="Book present in the stocks",
        )

    delete_books_stmt = delete_book_from_id_stmt(book_id)
    execute_statement(db_session, delete_books_stmt, is_commit=True)
