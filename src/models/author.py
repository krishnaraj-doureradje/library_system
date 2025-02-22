from datetime import date

from pydantic import BaseModel, ConfigDict
from sqlmodel import Field


class AuthorBase(BaseModel):
    """Pydantic base model to represent the author."""

    first_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        title="First Name",
    )
    last_name: str = Field(..., min_length=1, max_length=100, title="Last Name")
    birth_date: date
    nationality: str | None = Field(default=None, min_length=3, max_length=3, title="Nationality")

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "first_name": "John",
                    "last_name": "Doe",
                    "birth_date": "1980-05-15",
                    "nationality": "USA",
                }
            ]
        }
    )


class AuthorIn(AuthorBase):
    """Pydantic model to represent the author for input."""

    pass


class AuthorOut(AuthorBase):
    """Pydantic model to represent the author for output."""

    id: int = Field(
        ...,
        description="Created author ID",
    )
