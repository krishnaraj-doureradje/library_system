from sqlalchemy import Delete, Update, and_, delete, func, update
from sqlmodel import select
from sqlmodel.sql._expression_select_cls import SelectOfScalar

from src.db.models.admin_user import AdminUser
from src.db.models.author import Author
from src.db.models.book import Book
from src.db.models.reservation import Reservation
from src.db.models.reservation_status import ReservationStatus
from src.db.models.stock import Stock
from src.db.models.user import User


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


def delete_author_from_id_stmt(author_id: int) -> Delete:
    """This function return delete author statement

    Args:
        author_id (int): Author id to be deleted

    Returns:
         Delete: Delete statement
    """
    stmt = delete(Author).where(Author.id == author_id)  # type: ignore
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


def get_user_from_id_stmt(user_id: int) -> SelectOfScalar[User]:
    """This function returns a select statement to get the User.

    Args:
        user_id (int): The user id

    Returns:
        SelectOfScalar[User]: Select statement for user.
    """
    stmt = select(User).where(User.id == user_id)
    return stmt


def get_user_count_stmt() -> SelectOfScalar[int]:
    """This function returns a select statement to get the total number of users.

    Returns:
        SelectOfScalar[int]: Select statement for the count of user.
    """
    stmt = select(func.count().label("user_count")).select_from(User)
    return stmt


def get_users_stmt_with_limit_and_offset(*, offset: int, limit: int) -> SelectOfScalar[User]:
    """This function returns a select statement to get all users with pagination.

    Args:
        offset (int): Offset value.
        limit (int): Limit value.

    Returns:
        SelectOfScalar[User]: Select statement for all users.
    """
    stmt = select(User).limit(limit).offset(offset).order_by(User.id.asc())  # type: ignore
    return stmt


def get_reservation_status_stmt() -> SelectOfScalar[ReservationStatus]:
    """This function returns a select statement to get the reservation status.

    Returns:
        SelectOfScalar[ReservationStatus]: Select statement for reservation status.
    """
    stmt = select(ReservationStatus)
    return stmt


def get_non_returned_books_from_user_id_stmt(
    *, user_id: int, book_id: int
) -> SelectOfScalar[Reservation]:
    """This function returns a select statement to get non returned books.

    Args:
        user_id (int): User ID
        book_id (int): Book ID

    Returns:
        SelectOfScalar[Reservation]: Select statement for non returned books.
    """

    stmt = select(Reservation).where(
        and_(
            Reservation.user_id == user_id,  # type: ignore
            Reservation.book_id == book_id,  # type: ignore
            Reservation.returned_at.is_(None),  # type: ignore
        )
    )
    return stmt


def get_reservations_count_stmt() -> SelectOfScalar[int]:
    """This function returns a select statement to get the total number of reservations.

    Returns:
        SelectOfScalar[int]: Select statement for the reservations count.
    """
    stmt = select(func.count().label("reservation_count")).select_from(Reservation)
    return stmt


def get_reservations_stmt_with_limit_and_offset(
    *, offset: int, limit: int
) -> SelectOfScalar[Reservation]:
    """This function returns a select statement to get all reservations with pagination.

    Args:
        offset (int): Offset value.
        limit (int): Limit value.

    Returns:
        SelectOfScalar[Reservation]: Select statement for all Reservation.
    """
    stmt = select(Reservation).limit(limit).offset(offset).order_by(Reservation.id.asc())  # type: ignore
    return stmt


def get_reservation_from_id_stmt(reservation_id: int) -> SelectOfScalar[Reservation]:
    """This function returns a select statement to get the reservation.

    Args:
        reservation_id (int): The reservation id

    Returns:
        SelectOfScalar[Reservation]: Select statement for reservation.
    """
    stmt = select(Reservation).where(Reservation.id == reservation_id)
    return stmt


def get_reservation_books_from_id_stmt(
    *, reservation_id: int, user_id: int, book_id: int
) -> SelectOfScalar[Reservation]:
    """This function returns a select statement to get non returned books by using
       Reservation id, user_id & book_id.

    Args:
        reservation_id (int): Reservation ID
        user_id (int): User ID
        book_id (int): Book ID

    Returns:
        SelectOfScalar[Reservation]: Select statement for non returned books.
    """

    stmt = select(Reservation).where(
        and_(
            Reservation.id == reservation_id,  # type: ignore
            Reservation.user_id == user_id,  # type: ignore
            Reservation.book_id == book_id,  # type: ignore
            Reservation.returned_at.is_(None),  # type: ignore
        )
    )
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
