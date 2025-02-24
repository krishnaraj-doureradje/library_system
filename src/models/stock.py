from pydantic import BaseModel, ConfigDict, Field

from src.models.pagination import Pagination


class StockBase(BaseModel):
    """Pydantic model to represent the stock base."""

    book_id: int = Field(..., gt=0, title="Book ID")
    stock_quantity: int = Field(..., ge=0, title="Number of stock to be added")
    model_config = ConfigDict(json_schema_extra={"example": {"book_id": 6, "stock_quantity": 1}})


class StockIn(StockBase):
    """Pydantic model to represent the stock for input."""

    pass


class StockQuantityAdd(BaseModel):
    """Pydantic model to represent the stock update for input."""

    stock_quantity: int = Field(..., gt=0, title="Number of stock to be added")


class StockOut(StockBase):
    """Pydantic model to represent the stock for output."""

    id: int = Field(
        ...,
        description="Created stock ID",
    )
    title: str = Field(
        ...,
        min_length=1,
        max_length=100,
        title="Book title",
    )
    category: str | None = Field(default=None, min_length=1, max_length=100, title="Book's Title")


class StocksList(Pagination):
    """Pydantic model to represent a list of stocks."""

    number_of_stocks: int = Field(..., description="Total number of stocks")
    stocks: list[StockOut] = Field(..., description="List of available stocks")
