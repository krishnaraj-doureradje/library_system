from datetime import date

from pydantic import BaseModel, ConfigDict, Field

from src.models.pagination import Pagination


class BookBase(BaseModel):
    """Pydantic base model to represent the book."""

    title: str = Field(
        ...,
        min_length=1,
        max_length=100,
        title="Book title",
    )
    author_id: int = Field(..., gt=0, title="Author ID")
    published_date: date = Field(..., title="Book published date")

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "title": "Pride and Prejudice",
                    "author_id": 1,
                    "published_date": "1980-05-15",
                }
            ]
        }
    )


class BookIn(BookBase):
    """Pydantic model to represent the book for input."""

    pass


class BookOut(BookBase):
    """Pydantic model to represent the book for output."""

    id: int = Field(
        ...,
        description="Created book ID",
    )


class BooksList(Pagination):
    """Pydantic model to represent a list of books."""

    number_of_books: int = Field(..., description="Total number of books")
    books: list[BookOut] = Field(..., description="List of books")
