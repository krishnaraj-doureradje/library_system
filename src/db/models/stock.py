from datetime import datetime

from sqlalchemy import Column, DateTime, func
from sqlmodel import Field, SQLModel


class Stock(SQLModel, table=True):
    __tablename__ = "stocks"

    id: int | None = Field(default=None, primary_key=True, index=True, nullable=False)
    book_id: int = Field(foreign_key="books.id", index=True, nullable=False, unique=True)
    stock_quantity: int = Field(default=0, nullable=False)
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
