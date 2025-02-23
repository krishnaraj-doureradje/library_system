from fastapi import APIRouter, Depends

from src.db.engine import db_dependency
from src.db.operation import (
    create_user_on_db,
)
from src.models.error_response import ErrorResponse
from src.models.http_response_code import HTTPResponseCode
from src.models.user import UserIn, UserOut
from src.utils.security import user_is_authenticated

router = APIRouter(dependencies=[Depends(user_is_authenticated)])


@router.post(
    "/users",
    response_model=UserOut,
    responses={
        "401": {"model": ErrorResponse},
        "500": {"model": ErrorResponse},
    },
    summary="To create a new user.",
    tags=["Users"],
    status_code=HTTPResponseCode.CREATED,
)
async def create_user(
    db_session: db_dependency,
    user_in: UserIn,
) -> UserOut | ErrorResponse:
    new_user = create_user_on_db(db_session, user_in)
    return new_user
