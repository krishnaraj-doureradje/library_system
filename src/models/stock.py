from pydantic import BaseModel
from sqlmodel import Field


class StockBase(BaseModel):
    """Pydantic model to represent the stock base."""

    book_id: int = Field(..., gt=0, title="Book ID")
    stock_quantity: int = Field(..., gt=0, title="Number of stock to be added")


class StockIn(StockBase):
    """Pydantic model to represent the stock for input."""

    pass


class StockOut(StockBase):
    """Pydantic model to represent the stock for output."""

    id: int = Field(
        ...,
        description="Created stock ID",
    )
