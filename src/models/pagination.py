from pydantic import BaseModel, Field


class Pagination(BaseModel):
    """Pydantic model to represent pagination."""

    number_of_pages: int = Field(..., description="Total number of pages")
    current_page: int = Field(..., description="Current page")
    next_page: int | None = Field(..., description="Next page")
    previous_page: int | None = Field(..., description="Previous page")
