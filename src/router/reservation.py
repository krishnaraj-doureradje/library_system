from fastapi import APIRouter, Depends, Path

from src.db.engine import db_dependency
from src.db.operations.reservation import (
    create_reservation_on_db,
    get_reservation_out_from_db,
    get_reservations_with_offset_and_limit,
    update_reservation_on_db,
)
from src.helper.pagination import pager_params_dependency
from src.models.error_response import ErrorResponse
from src.models.http_response_code import HTTPResponseCode
from src.models.reservation import ReservationIn, ReservationOut, ReservationsList
from src.utils.security import user_is_authenticated

router = APIRouter(dependencies=[Depends(user_is_authenticated)])


@router.post(
    "/reservations",
    response_model=ReservationOut,
    responses={
        "400": {"model": ErrorResponse},
        "401": {"model": ErrorResponse},
        "404": {"model": ErrorResponse},
        "500": {"model": ErrorResponse},
    },
    summary="To reserve a book.",
    tags=["Reservations"],
    status_code=HTTPResponseCode.CREATED,
)
async def create_reservation(
    db_session: db_dependency,
    reservation_in: ReservationIn,
) -> ReservationOut | ErrorResponse:
    new_reservation = create_reservation_on_db(db_session, reservation_in)
    return new_reservation


@router.get(
    "/reservations/{reservation_id}",
    response_model=ReservationOut,
    responses={
        "401": {"model": ErrorResponse},
        "404": {"model": ErrorResponse},
        "500": {"model": ErrorResponse},
    },
    summary="To get a reservation based on the reservation id.",
    tags=["Reservations"],
)
async def get_reservation(
    db_session: db_dependency,
    reservation_id: int = Path(
        ...,
        title="Reservation ID",
        examples=[1],
    ),
) -> ReservationOut | ErrorResponse:
    reservation_out = get_reservation_out_from_db(db_session, reservation_id)
    return reservation_out


@router.get(
    "/reservations",
    response_model=ReservationsList,
    responses={
        "401": {"model": ErrorResponse},
        "500": {"model": ErrorResponse},
    },
    summary="To get all reservations from the database with pagination.",
    tags=["Reservations"],
)
async def get_all_reservations(
    db_session: db_dependency,
    pager_params: pager_params_dependency,
) -> ReservationsList | ErrorResponse:
    reservations = get_reservations_with_offset_and_limit(
        db_session,
        offset=pager_params["skip"],
        limit=pager_params["limit"],
    )
    return reservations


@router.put(
    "/reservations/{reservation_id}",
    response_model=ReservationOut,
    responses={
        "400": {"model": ErrorResponse},
        "401": {"model": ErrorResponse},
        "404": {"model": ErrorResponse},
        "500": {"model": ErrorResponse},
    },
    summary="To return a borrowed book.",
    tags=["Reservations"],
)
async def update_reservation(
    db_session: db_dependency,
    reservation_in: ReservationIn,
    reservation_id: int = Path(..., title="Reservation ID", examples=[1]),
) -> ReservationOut | ErrorResponse:
    updated_reservation = update_reservation_on_db(db_session, reservation_id, reservation_in)
    return updated_reservation
