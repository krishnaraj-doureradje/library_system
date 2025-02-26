from src.db.engine import db_dependency
from src.db.execution import delete_statement, execute_all_query, fetch_all, fetch_one_or_none
from src.db.models.author import Author
from src.db.queries.admin_user import get_author_count_stmt, get_authors_stmt_with_limit_and_offset
from src.db.queries.author import delete_author_from_id_stmt, get_author_stmt
from src.db.queries.book import (
    delete_books_from_author_id_stmt,
)
from src.exceptions.app import NotFoundException, SqlException
from src.helper.pagination import pagination_details
from src.models.author import AuthorIn, AuthorOut, AuthorsList
from src.models.http_response_code import HTTPResponseCode


def create_author_on_db(db_session: db_dependency, author_in: AuthorIn) -> AuthorOut:
    """Create a new author in the databases

    Args:
        db_session (db_dependency): Database session.
        author_in (AuthorIn): Author details

    Returns:
        AuthorOut: Author details with ID
    """
    new_author = Author(**author_in.model_dump())
    # Refresh the object after commit to get the primary key
    execute_all_query(db_session, [new_author], is_commit=True, is_refresh_after_commit=True)
    return AuthorOut(**new_author.model_dump())


def get_author_from_id(db_session: db_dependency, author_id: int) -> Author:
    """Get an author based on the author id.

    Args:
        db_session (db_dependency):  Database session.
        author_id (int): Author id

    Raises:
        NotFoundException: Raised when the author id is not found in the database.

    Returns:
        Author: Author details
    """
    author_stmt = get_author_stmt(author_id)
    author = fetch_one_or_none(db_session, author_stmt)

    if author is None:
        raise NotFoundException(
            status_code=HTTPResponseCode.NOT_FOUND,
            message=f"{author_id=} not found in the database",
        )

    return author


def get_author_out_from_db(db_session: db_dependency, author_id: int) -> AuthorOut:
    """Get AuthorOut model response.

    Args:
        db_session (db_dependency): Database session.
        author_id (int): Author id.

    Returns:
        AuthorOut: Author details.
    """
    db_author = get_author_from_id(db_session, author_id)
    return AuthorOut(**db_author.model_dump())


def get_authors_with_offset_and_limit(
    db_session: db_dependency, *, offset: int, limit: int
) -> AuthorsList:
    """Get all authors with pagination.

    Args:
        db_session (db_dependency): Database session.
        offset (int): Offset value.
        limit (int): Limit value.

    Returns:
        AuthorsList: List of authors.
    """
    authors_count_stmt = get_author_count_stmt()
    authors_count = fetch_one_or_none(db_session, authors_count_stmt)  # type: ignore

    # There is nothing to fetch if the authors_count is None
    if authors_count is None:
        return AuthorsList(
            authors=[],
            number_of_authors=0,
            number_of_pages=0,
            current_page=0,
            next_page=None,
            previous_page=None,
        )

    authors_stmt = get_authors_stmt_with_limit_and_offset(offset=offset, limit=limit)
    authors = [AuthorOut(**author.model_dump()) for author in fetch_all(db_session, authors_stmt)]

    # Calculate the number of pages, current page, next page, and previous page
    number_of_pages, current_page, next_page, previous_page = pagination_details(
        offset=offset, limit=limit, counts=authors_count
    )

    return AuthorsList(
        authors=authors,
        number_of_authors=authors_count,
        number_of_pages=number_of_pages,
        current_page=current_page,
        next_page=next_page,
        previous_page=previous_page,
    )


def update_author_on_db(
    db_session: db_dependency, author_id: int, author_in: AuthorIn
) -> AuthorOut:
    """Update a author based on the author id.

    Args:
        db_session (db_dependency): Database session.
        author_id (int): Author id.
        author_in (AuthorIn): Author details.

    Raises:
        NotFoundException: Raised when the author id is not found in the database.

    Returns:
        AuthorOut: Updated author details.
    """
    db_author = get_author_from_id(db_session, author_id)

    # Update the author fields with the new values
    for field, value in author_in.model_dump().items():
        setattr(db_author, field, value)

    author_out = AuthorOut(**db_author.model_dump())
    # We don't need to refresh the object for the update operation, so we can avoid
    # making a select request to the database.
    execute_all_query(
        db_session,
        [db_author],  # type: ignore
    )
    return author_out


def delete_author_on_db(
    db_session: db_dependency,
    author_id: int,
) -> None:
    """Delete a author based on the author id.

    Args:
        db_session (db_dependency): Database session.
        author_id (int): Author id.
    """
    try:
        db_author = get_author_from_id(db_session, author_id)
    except NotFoundException:
        # Nothing to delete so don't raise exception
        return None

    is_stock_present = any(book.stock for book in db_author.books)
    if is_stock_present:
        raise SqlException(
            status_code=HTTPResponseCode.FORBIDDEN,
            message="Author's book present in the stocks",
        )

    delete_books_stmt = delete_books_from_author_id_stmt(author_id)
    delete_author_stmt = delete_author_from_id_stmt(author_id)
    delete_statement(db_session, delete_books_stmt, is_commit=False)
    delete_statement(db_session, delete_author_stmt, is_commit=True)
