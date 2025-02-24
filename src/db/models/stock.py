from datetime import datetime

from sqlalchemy import Column, DateTime, func
from sqlmodel import Field, Relationship, SQLModel


class Stock(SQLModel, table=True):
    __tablename__ = "stocks"

    id: int | None = Field(default=None, primary_key=True, index=True, nullable=False)
    book_id: int = Field(foreign_key="books.id", index=True, nullable=False, unique=True)
    stock_quantity: int = Field(default=0, nullable=False, ge=0)
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
    book: "Book" = Relationship(back_populates="stock")  # type: ignore  # noqa: F821

    def __repr__(self) -> str:
        return (
            f"<Stock(id={self.id}, book_id={self.book_id}, stock_quantity={self.stock_quantity})>"
        )
