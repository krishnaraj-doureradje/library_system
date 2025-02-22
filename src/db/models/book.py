from datetime import date, datetime

from sqlalchemy import Column, DateTime, UniqueConstraint, func
from sqlmodel import Field, SQLModel


class Book(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, index=True, nullable=False)
    title: str = Field(nullable=False, max_length=255)
    author_id: int = Field(foreign_key="author.id", index=True, nullable=False)
    published_date: date = Field(nullable=False)
    category: str | None = Field(default=None, max_length=100)
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
    __table_args__ = (
        UniqueConstraint(
            "title", "author_id", "published_date", name="uq_title_authorid_publish_date"
        ),
    )

    def __repr__(self) -> str:
        return f"<Book(title={self.title}, author_id={self.author_id})>"
