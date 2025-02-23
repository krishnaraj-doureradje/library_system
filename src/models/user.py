from pydantic import BaseModel, ConfigDict, EmailStr, Field

from src.models.pagination import Pagination


class UserBase(BaseModel):
    """Pydantic base model to represent the User."""

    first_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        title="First Name",
    )
    last_name: str = Field(..., min_length=1, max_length=100, title="Last Name")
    email: EmailStr

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
            }
        }
    )


class UserIn(UserBase):
    """Pydantic model to represent the user for input."""

    pass


class UserOut(UserBase):
    """Pydantic model to represent the user for output."""

    id: int = Field(
        ...,
        description="Created user ID",
    )


class UsersList(Pagination):
    """Pydantic model to represent a list of users."""

    number_of_users: int = Field(..., description="Total number of users")
    users: list[UserOut] = Field(..., description="List of users")
