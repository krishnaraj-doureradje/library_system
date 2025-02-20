from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """App ErrorResponse Model."""

    code: str | None
    message: str | None
