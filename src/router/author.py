from fastapi import APIRouter, Depends

from src.db.engine import db_dependency
from src.db.operation import (
    create_author_on_db,
)
from src.models.author import (
    AuthorIn,
    AuthorOut,
)
from src.models.error_response import ErrorResponse
from src.models.http_response_code import HTTPResponseCode
from src.utils.security import user_is_authenticated

router = APIRouter(dependencies=[Depends(user_is_authenticated)])


@router.post(
    "/authors",
    response_model=AuthorOut,
    responses={
        "401": {"model": ErrorResponse},
        "500": {"model": ErrorResponse},
    },
    summary="To create a new author.",
    tags=["Authors"],
    status_code=HTTPResponseCode.CREATED,
)
async def create_author(
    db_session: db_dependency,
    author_in: AuthorIn,
) -> AuthorOut | ErrorResponse:
    new_author = create_author_on_db(db_session, author_in)
    return new_author
