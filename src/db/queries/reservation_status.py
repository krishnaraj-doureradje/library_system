from sqlmodel import select
from sqlmodel.sql._expression_select_cls import SelectOfScalar

from src.db.models.reservation_status import ReservationStatus


def get_reservation_status_stmt() -> SelectOfScalar[ReservationStatus]:
    """This function returns a select statement to get the reservation status.

    Returns:
        SelectOfScalar[ReservationStatus]: Select statement for reservation status.
    """
    stmt = select(ReservationStatus)
    return stmt
