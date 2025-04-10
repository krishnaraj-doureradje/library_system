import logging
from contextlib import contextmanager
from datetime import datetime, timedelta
from functools import lru_cache

from src.db.engine import db_dependency, get_db_session
from src.db.execution import execute_all_query, execute_statements, fetch_all, fetch_one_or_none
from src.db.models.reservation import Reservation
from src.db.queries.reservation import (
    get_non_returned_books_from_user_id_stmt,
    get_reservation_books_from_id_stmt,
    get_reservation_from_id_stmt,
    get_reservations_count_stmt,
    get_reservations_stmt_with_limit_and_offset,
)
from src.db.queries.reservation_status import get_reservation_status_stmt
from src.db.queries.stock import (
    get_decrement_stock_quantity_stmt,
    get_increment_stock_quantity_stmt,
    get_stock_book_stmt,
)
from src.db.queries.user import get_user_from_id_stmt
from src.exceptions.app import NotFoundException, ReservationException
from src.helper.pagination import pagination_details
from src.models.http_response_code import HTTPResponseCode
from src.models.reservation import ReservationIn, ReservationOut, ReservationsList
from src.models.reservation_status import ReservationStatus

logger = logging.getLogger("app")


def create_reservation_on_db(
    db_session: db_dependency, reservation_in: ReservationIn
) -> ReservationOut:
    """Create a reservation in the databases

    Args:
        db_session (db_dependency): Database session.
        reservation_in (ReservationIn): Reservation details

    Returns:
        ReservationOut: Reservation details with ID
    """
    verify_user_and_reservation(db_session, reservation_in)
    verify_stock_quantity_for_reservation(db_session, reservation_in.book_id)

    # Get reservation status
    reservation_status = {value: key for key, value in get_reservation_status_dict().items()}

    new_reservation = Reservation(
        book_id=reservation_in.book_id,
        user_id=reservation_in.user_id,
        status_id=reservation_status[ReservationStatus.CONFIRMED.value],
        due_date=datetime.now() + timedelta(days=15),
        borrowed_at=datetime.now(),
        returned_at=None,
    )
    # Decrement stock quantity by one and commit it the execute_all_query
    decrement_stock_quantity_stmt = get_decrement_stock_quantity_stmt(reservation_in.book_id)
    execute_statements(db_session, [decrement_stock_quantity_stmt], is_commit=False)

    # Refresh the object after commit to get the primary key
    execute_all_query(
        db_session,
        [
            new_reservation,
        ],
        is_commit=True,
        is_refresh_after_commit=True,
    )
    return ReservationOut(
        id=new_reservation.id,  # type: ignore
        book_id=reservation_in.book_id,
        user_id=reservation_in.user_id,
        status=ReservationStatus.CONFIRMED.value,
        due_date=datetime.now() + timedelta(days=15),
        borrowed_at=datetime.now(),
        return_date=None,
    )


def verify_user_and_reservation(db_session: db_dependency, reservation_in: ReservationIn) -> None:
    """Method is used to verify user and reservation logic.

    Args:
        db_session (db_dependency): Database session.
        reservation_in (ReservationIn): Reservation details

    Raises:
        NotFoundException: Item not found in the databases
        ReservationException: Not valid request to reserve
    """
    user_id = reservation_in.user_id
    book_id = reservation_in.book_id

    user_stmt = get_user_from_id_stmt(user_id)
    user = fetch_one_or_none(db_session, user_stmt)
    if user is None:
        raise NotFoundException(
            status_code=HTTPResponseCode.NOT_FOUND,
            message=f"{user_id=} not found in the database",
        )

    non_returned_books_stmt = get_non_returned_books_from_user_id_stmt(
        user_id=user_id, book_id=book_id
    )
    non_returned_books = fetch_one_or_none(db_session, non_returned_books_stmt)

    if non_returned_books:
        raise ReservationException(
            status_code=HTTPResponseCode.BAD_REQUEST,
            message=f"Book already borrowed {book_id=} and due date {non_returned_books.due_date}",
        )


def verify_stock_quantity_for_reservation(db_session: db_dependency, book_id: int) -> None:
    """To verify stock details from book_id, it's available for assignment.

    Args:
        db_session (db_dependency): Database session.
        book_id (int): Book ID

    Raises:
        NotFoundException: Item not found in the databases
        ReservationException: Not valid request to reserve
    """
    stock_stmt = get_stock_book_stmt(book_id)
    stock = fetch_one_or_none(db_session, stock_stmt)

    if stock is None:
        raise NotFoundException(
            status_code=HTTPResponseCode.NOT_FOUND,
            message=f"{book_id=} not found in the database",
        )

    if not (stock.stock_quantity > 0):
        raise ReservationException(
            status_code=HTTPResponseCode.BAD_REQUEST,
            message=f"{book_id=} not available for reservations",
        )


def get_reservations_from_user_id(db_session: db_dependency, reservation_id: int) -> Reservation:
    """Get all the reservations of given reservation_id.

    Args:
        db_session (db_dependency):  Database session.
        reservation_id (int): Reservation id

    Raises:
        NotFoundException: Raised when the reservation id is not found in the database.

    Returns:
        Reservation: Reservation details
    """
    reservation_stmt = get_reservation_from_id_stmt(reservation_id)
    reservation = fetch_one_or_none(db_session, reservation_stmt)

    if reservation is None:
        raise NotFoundException(
            status_code=HTTPResponseCode.NOT_FOUND,
            message=f"{reservation_id=} not found in the database",
        )

    return reservation


def get_reservation_out_from_db(db_session: db_dependency, reservation_id: int) -> ReservationOut:
    """Get reservation out model response.

    Args:
        db_session (db_dependency): Database session.
        reservation_id (int): Reservation id.

    Returns:
        ReservationOut: Reservation details.
    """
    db_reservation = get_reservations_from_user_id(db_session, reservation_id)
    # Get reservation status
    reservation_status = get_reservation_status_dict()

    return ReservationOut(
        id=db_reservation.id,  # type: ignore
        book_id=db_reservation.book_id,
        user_id=db_reservation.user_id,
        status=reservation_status[db_reservation.status_id],
        due_date=db_reservation.due_date,
        borrowed_at=db_reservation.borrowed_at,
        return_date=db_reservation.returned_at,
    )


def get_reservations_with_offset_and_limit(
    db_session: db_dependency, *, offset: int, limit: int
) -> ReservationsList:
    """Get all the reservations with pagination.

    Args:
        db_session (db_dependency): Database session.
        offset (int): Offset value.
        limit (int): Limit value.

    Returns:
        ReservationsList: List of reservations.
    """
    reservations_count_stmt = get_reservations_count_stmt()
    reservation_count = fetch_one_or_none(db_session, reservations_count_stmt)  # type: ignore

    # There is nothing to fetch if the reservation_count is None
    if reservation_count is None:
        return ReservationsList(
            reservations=[],
            number_of_reservation=0,
            number_of_pages=0,
            current_page=0,
            next_page=None,
            previous_page=None,
        )

    # Get reservation status
    reservation_status = get_reservation_status_dict()

    reservations_stmt = get_reservations_stmt_with_limit_and_offset(offset=offset, limit=limit)
    reservations: list[ReservationOut] = []
    for reservation in fetch_all(db_session, reservations_stmt):
        res_out = ReservationOut(
            id=reservation.id,  # type: ignore
            book_id=reservation.book_id,
            user_id=reservation.user_id,
            status=reservation_status[reservation.status_id],
            due_date=reservation.due_date,
            borrowed_at=reservation.borrowed_at,
            return_date=reservation.returned_at,
        )
        reservations.append(res_out)

    # Calculate the number of pages, current page, next page, and previous page
    number_of_pages, current_page, next_page, previous_page = pagination_details(
        offset=offset, limit=limit, counts=reservation_count
    )

    return ReservationsList(
        reservations=reservations,
        number_of_reservation=reservation_count,
        number_of_pages=number_of_pages,
        current_page=current_page,
        next_page=next_page,
        previous_page=previous_page,
    )


def update_reservation_on_db(  # noqa: PLR0915
    db_session: db_dependency, reservation_id: int, reservation_in: ReservationIn
) -> ReservationOut:
    """Update an reservation based on the reservation_id, user_id and book_id.

    Args:
        db_session (db_dependency): Database session.
        reservation_id (int): Reservation id.
        reservation_in (reservation_in): ReservationIn.

    Raises:
        NotFoundException: Raised when the user id is not found in the database.

    Returns:
        ReservationOut: Reservation details.
    """
    verify_reservation(db_session, reservation_in, reservation_id)

    stock_stmt = get_stock_book_stmt(reservation_in.book_id)
    stock = fetch_one_or_none(db_session, stock_stmt)

    if stock is None:
        raise NotFoundException(
            status_code=HTTPResponseCode.NOT_FOUND,
            message=f"{reservation_in.book_id=} not found in the database",
        )

    reservation = get_reservations_from_user_id(db_session, reservation_id)
    # Get reservation status
    reservation_status = {value: key for key, value in get_reservation_status_dict().items()}

    # Update db with return date and status
    reservation.returned_at = datetime.now()
    reservation.status_id = reservation_status[ReservationStatus.RETURNED.value]

    # Increase stock after return and commit it below in the execute_all_query
    increment_stock_quantity_stmt = get_increment_stock_quantity_stmt(reservation_in.book_id)
    execute_statements(db_session, [increment_stock_quantity_stmt], is_commit=False)

    # Refresh reservation and stock object
    execute_all_query(
        db_session, [reservation, stock], is_commit=True, is_refresh_after_commit=True
    )
    return ReservationOut(
        id=reservation.id,  # type: ignore
        book_id=reservation.book_id,
        user_id=reservation.user_id,
        status=ReservationStatus.RETURNED.value,
        due_date=reservation.due_date,
        borrowed_at=reservation.borrowed_at,
        return_date=reservation.returned_at,
    )


def verify_reservation(
    db_session: db_dependency, reservation_in: ReservationIn, reservation_id: int
) -> None:
    """Verify book return condition

    Args:
        db_session (db_dependency): Database session.
        reservation_in (reservation_in): ReservationIn.
        reservation_id (int): Reservation ID.

    Raises:
        ReservationException: If the reservation is not found in the database
    """
    user_id = reservation_in.user_id
    book_id = reservation_in.book_id

    non_returned_books_stmt = get_reservation_books_from_id_stmt(
        reservation_id=reservation_id, user_id=user_id, book_id=book_id
    )
    non_returned_books = fetch_one_or_none(db_session, non_returned_books_stmt)

    if non_returned_books is None:
        raise ReservationException(
            status_code=HTTPResponseCode.BAD_REQUEST,
            message=(
                f"Book not borrowed | user or reservation not found {book_id=}, "
                f"{user_id=}, {reservation_id=}"
            ),
        )


@lru_cache
def get_reservation_status_dict() -> dict[int, str]:
    """Get reservation status as dict format.

    Returns:
        dict[int, str]: Return reservation status
    """
    reservation_status_stmt = get_reservation_status_stmt()

    with contextmanager(get_db_session)() as session:
        reservation_status: dict[int, str] = {
            reservation.id: reservation.name  # type: ignore
            for reservation in fetch_all(session, reservation_status_stmt)
        }

    return reservation_status
