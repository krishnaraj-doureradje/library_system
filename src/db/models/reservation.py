from datetime import datetime

from sqlalchemy import Column, DateTime, func
from sqlmodel import Field, SQLModel


class Reservation(SQLModel, table=True):
    __tablename__ = "reservations"

    id: int | None = Field(default=None, primary_key=True, index=True, nullable=False)
    book_id: int = Field(foreign_key="books.id", nullable=False, index=True)
    user_id: int = Field(foreign_key="users.id", nullable=False, index=True)
    status_id: int = Field(foreign_key="reservation_status.id", nullable=False)
    borrowed_at: datetime = Field(
        sa_column=Column(
            DateTime,
            server_default=func.now(),
            nullable=False,
        ),
    )
    due_date: datetime = Field(nullable=False)
    returned_at: datetime | None = None

    def __repr__(self) -> str:
        return f"<Reservation(id={self.id}, book_id={self.book_id}, user_id={self.user_id})>"
