from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from src.models.pagination import Pagination


class ReservationBase(BaseModel):
    """Pydantic base model to represent the reservation."""

    book_id: int = Field(..., gt=0, title="Book ID")
    user_id: int = Field(..., gt=0, title="User ID")

    model_config = ConfigDict(json_schema_extra={"example": {"book_id": 123, "user_id": 456}})


class ReservationIn(ReservationBase):
    """Pydantic model to represent the reservation for input."""

    pass


class ReservationOut(ReservationBase):
    """Pydantic base model to represent the reservation."""

    id: int = Field(..., gt=0, title="Reservation ID")
    status: str = Field(..., title="Reservation status")
    borrowed_at: datetime = Field(..., title="Borrowed datetime")
    due_date: datetime = Field(..., title="Due date")
    return_date: datetime | None = Field(..., title="Due date")


class ReservationsList(Pagination):
    """Pydantic model to represent a list of reservations."""

    number_of_reservation: int = Field(..., description="Total number of reservations")
    reservations: list[ReservationOut] = Field(..., description="List of reservations")
