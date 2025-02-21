from datetime import datetime

from sqlalchemy import Column, DateTime, func
from sqlmodel import Field, SQLModel


class Author(SQLModel, table=True):
    """Pydantic model to represent an author in the database."""

    id: int | None = Field(default=None, primary_key=True, index=True, nullable=False)
    first_name: str = Field(index=True, nullable=False, max_length=100)
    last_name: str = Field(index=True, nullable=False, max_length=100)
    birth_date: datetime | None = None
    nationality: str | None = Field(default=None, min_length=3, max_length=3)
    created_at: datetime = Field(
        sa_column=Column(
            DateTime,
            server_default=func.now(),
            nullable=False,
        ),
    )

    updated_at: datetime = Field(
        sa_column=Column(
            DateTime,
            server_default=func.now(),
            onupdate=func.now(),
            nullable=False,
        ),
    )

    def __repr__(self):
        return f"<Author(id={self.id}, name={self.first_name} {self.last_name})>"
