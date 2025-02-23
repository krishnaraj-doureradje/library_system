from src.db.engine import db_dependency
from src.db.execution import delete_statement, execute_all_query, fetch_all, fetch_one_or_none
from src.db.models.admin_user import AdminUser
from src.db.models.author import Author
from src.db.models.book import Book
from src.db.models.stock import Stock
from src.db.models.user import User
from src.db.query import (
    delete_author_from_id_stmt,
    delete_book_from_id_stmt,
    get_admin_user_stmt,
    get_author_count_stmt,
    get_author_stmt,
    get_authors_stmt_with_limit_and_offset,
    get_book_count_stmt,
    get_book_from_id_stmt,
    get_books_stmt_with_limit_and_offset,
    get_stock_book_stmt,
    get_stocks_count_stmt,
    get_stocks_stmt_with_limit_and_offset,
    get_user_count_stmt,
    get_user_from_id_stmt,
    get_users_stmt_with_limit_and_offset,
)
from src.exceptions.app import NotFoundException, SqlException
from src.helper.pagination import pagination_details
from src.models.author import AuthorIn, AuthorOut, AuthorsList
from src.models.book import BookIn, BookOut, BooksList
from src.models.http_response_code import HTTPResponseCode
from src.models.stock import StockIn, StockOut, StockQuantityAdd, StocksList
from src.models.user import UserIn, UserOut, UsersList


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


def get_admin_user(db_session: db_dependency, user_id: str) -> AdminUser | None:
    """Retrieve an admin user from the database.

    Args:
        db_session (db_dependency): Databases sessions.
        user_id (str): Admin user_id

    Returns:
        AdminUser | None: The corresponding AdminUser object if found, otherwise None.
    """
    admin_user_stmt = get_admin_user_stmt(user_id)
    admin_user = fetch_one_or_none(db_session, admin_user_stmt)
    return admin_user


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
    """Get an stock based on the book id.

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
    """Get all stocks with pagination.

    Args:
        db_session (db_dependency): Database session.
        offset (int): Offset value.
        limit (int): Limit value.

    Returns:
        StocksList: List of available stocks.
    """
    stocks_count_stmt = get_stocks_count_stmt()
    stocks_count = fetch_one_or_none(db_session, stocks_count_stmt)  # type: ignore

    # There is nothing to fetch if the authors_count is None
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
    stocks = []
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
    db_stock = get_stock_book_from_id(db_session, book_id)
    # Add new quantity to the stocks
    db_stock.stock_quantity += stock_in.stock_quantity

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

    delete_books_stmt = delete_book_from_id_stmt(author_id)
    delete_author_stmt = delete_author_from_id_stmt(author_id)
    delete_statement(db_session, delete_books_stmt, is_commit=False)
    delete_statement(db_session, delete_author_stmt, is_commit=True)


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
    delete_statement(db_session, delete_books_stmt, is_commit=True)


def create_user_on_db(db_session: db_dependency, user_in: UserIn) -> UserOut:
    """Create a new user in the databases

    Args:
        db_session (db_dependency): Database session.
        user_in (UserIn): User details

    Returns:
        UserOut: User details with ID
    """
    new_user = User(**user_in.model_dump())
    # Refresh the object after commit to get the primary key
    execute_all_query(db_session, [new_user], is_commit=True, is_refresh_after_commit=True)
    return UserOut(**new_user.model_dump())


def get_user_from_id(db_session: db_dependency, user_id: int) -> User:
    """Get an user based on the user id.

    Args:
        db_session (db_dependency):  Database session.
        user_id (int): User id

    Raises:
        NotFoundException: Raised when the user id is not found in the database.

    Returns:
        User: User details
    """
    user_stmt = get_user_from_id_stmt(user_id)
    user = fetch_one_or_none(db_session, user_stmt)

    if user is None:
        raise NotFoundException(
            status_code=HTTPResponseCode.NOT_FOUND,
            message=f"{user_id=} not found in the database",
        )

    return user


def get_user_out_from_db(db_session: db_dependency, user_id: int) -> UserOut:
    """Get userOut model response.

    Args:
        db_session (db_dependency): Database session.
        user_id (int): User id.

    Returns:
        UserOut: User details.
    """
    db_user = get_user_from_id(db_session, user_id)
    return UserOut(**db_user.model_dump())


def get_users_with_offset_and_limit(
    db_session: db_dependency, *, offset: int, limit: int
) -> UsersList:
    """Get all users with pagination.

    Args:
        db_session (db_dependency): Database session.
        offset (int): Offset value.
        limit (int): Limit value.

    Returns:
        UsersList: List of authors.
    """
    users_count_stmt = get_user_count_stmt()
    users_count = fetch_one_or_none(db_session, users_count_stmt)  # type: ignore

    # There is nothing to fetch if the authors_count is None
    if users_count is None:
        return UsersList(
            users=[],
            number_of_users=0,
            number_of_pages=0,
            current_page=0,
            next_page=None,
            previous_page=None,
        )

    users_stmt = get_users_stmt_with_limit_and_offset(offset=offset, limit=limit)
    users = [UserOut(**user.model_dump()) for user in fetch_all(db_session, users_stmt)]

    # Calculate the number of pages, current page, next page, and previous page
    number_of_pages, current_page, next_page, previous_page = pagination_details(
        offset=offset, limit=limit, counts=users_count
    )

    return UsersList(
        users=users,
        number_of_users=users_count,
        number_of_pages=number_of_pages,
        current_page=current_page,
        next_page=next_page,
        previous_page=previous_page,
    )


def update_user_on_db(db_session: db_dependency, user_id: int, user_in: UserIn) -> UserOut:
    """Update an user based on the user id.

    Args:
        db_session (db_dependency): Database session.
        user_id (int): User id.
        user_in (UserIn): User details.

    Raises:
        NotFoundException: Raised when the user id is not found in the database.

    Returns:
        UserOut: Updated user details.
    """
    db_user = get_user_from_id(db_session, user_id)

    # Update the author fields with the new values
    for field, value in user_in.model_dump().items():
        setattr(db_user, field, value)

    user_out = UserOut(**db_user.model_dump())
    # We don't need to refresh the object for the update operation, so we can avoid
    # making a select request to the database.
    execute_all_query(
        db_session,
        [db_user],  # type: ignore
    )
    return user_out
