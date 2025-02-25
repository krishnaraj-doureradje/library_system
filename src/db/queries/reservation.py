from sqlalchemy import and_, func
from sqlmodel import select
from sqlmodel.sql._expression_select_cls import SelectOfScalar

from src.db.models.reservation import Reservation


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
