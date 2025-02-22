from typing import List

from sqlmodel import Field, Relationship, SQLModel


class ReservationStatus(SQLModel, table=True):
    __tablename__ = "reservation_status"

    id: int | None = Field(default=None, primary_key=True, index=True, nullable=False)
    name: str = Field(unique=True, nullable=False, max_length=32)

    reservations: List["Reservation"] = Relationship(back_populates="status")  # type: ignore # noqa: F821
