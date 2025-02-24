from datetime import datetime

from sqlalchemy import Column, DateTime, func
from sqlmodel import Field, SQLModel


class AdminUser(SQLModel, table=True):
    """Model for admin users with authentication."""

    __tablename__ = "admin_users"
    id: int | None = Field(default=None, primary_key=True)
    user_id: str = Field(nullable=False, max_length=255, index=True, unique=True)
    password: str = Field(nullable=False, max_length=255)
    created_at: datetime = Field(
        sa_column=Column(
            DateTime,
            server_default=func.now(),
            nullable=False,
        )
    )

    def __repr__(self) -> str:
        """String representation for debugging/logging."""
        return f"<AdminUser(id={self.id}, user_id={self.user_id},created_at={self.created_at})>"
