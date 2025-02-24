from fastapi import APIRouter, Depends, Path

from src.db.engine import db_dependency
from src.db.operations.user import (
    create_user_on_db,
    get_user_out_from_db,
    get_users_with_offset_and_limit,
    update_user_on_db,
)
from src.helper.pagination import pager_params_dependency
from src.models.error_response import ErrorResponse
from src.models.http_response_code import HTTPResponseCode
from src.models.user import UserIn, UserOut, UsersList
from src.utils.security import user_is_authenticated

router = APIRouter(dependencies=[Depends(user_is_authenticated)])


@router.post(
    "/users",
    response_model=UserOut,
    responses={
        "401": {"model": ErrorResponse},
        "500": {"model": ErrorResponse},
    },
    summary="To create a new user (email should be unique).",
    tags=["Users"],
    status_code=HTTPResponseCode.CREATED,
)
async def create_user(
    db_session: db_dependency,
    user_in: UserIn,
) -> UserOut | ErrorResponse:
    new_user = create_user_on_db(db_session, user_in)
    return new_user


@router.get(
    "/users/{user_id}",
    response_model=UserOut,
    responses={
        "401": {"model": ErrorResponse},
        "404": {"model": ErrorResponse},
        "500": {"model": ErrorResponse},
    },
    summary="To get an user based on the user id.",
    tags=["Users"],
)
async def get_user(
    db_session: db_dependency,
    user_id: int = Path(
        ...,
        title="User ID",
        examples=[1],
    ),
) -> UserOut | ErrorResponse:
    user_out = get_user_out_from_db(db_session, user_id)
    return user_out


@router.get(
    "/users",
    response_model=UsersList,
    responses={
        "401": {"model": ErrorResponse},
        "500": {"model": ErrorResponse},
    },
    summary="To get all users from the database with pagination.",
    tags=["Users"],
)
async def get_all_users(
    db_session: db_dependency,
    pager_params: pager_params_dependency,
) -> UsersList | ErrorResponse:
    users = get_users_with_offset_and_limit(
        db_session,
        offset=pager_params["skip"],
        limit=pager_params["limit"],
    )
    return users


@router.put(
    "/users/{user_id}",
    response_model=UserOut,
    responses={
        "401": {"model": ErrorResponse},
        "404": {"model": ErrorResponse},
        "500": {"model": ErrorResponse},
    },
    summary="To update an user based on the user id",
    tags=["Users"],
)
async def update_user(
    db_session: db_dependency,
    user_in: UserIn,
    user_id: int = Path(..., title="User ID", examples=[1]),
) -> UserOut | ErrorResponse:
    updated_user = update_user_on_db(db_session, user_id, user_in)
    return updated_user
