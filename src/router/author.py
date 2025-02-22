from fastapi import APIRouter, Depends, Path

from src.db.engine import db_dependency
from src.db.operation import (
    create_author_on_db,
    delete_author_on_db,
    get_author_out_from_db,
    get_authors_with_offset_and_limit,
    update_author_on_db,
)
from src.helper.pagination import pager_params_dependency
from src.models.author import (
    AuthorIn,
    AuthorOut,
    AuthorsList,
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


@router.get(
    "/authors/{author_id}",
    response_model=AuthorOut,
    responses={
        "401": {"model": ErrorResponse},
        "404": {"model": ErrorResponse},
        "500": {"model": ErrorResponse},
    },
    summary="To get an author based on the author id.",
    tags=["Authors"],
)
async def get_author(
    db_session: db_dependency,
    author_id: int = Path(
        ...,
        title="Author ID",
        examples=[1],
    ),
) -> AuthorOut | ErrorResponse:
    author_out = get_author_out_from_db(db_session, author_id)
    return author_out


@router.get(
    "/authors",
    response_model=AuthorsList,
    responses={
        "401": {"model": ErrorResponse},
        "500": {"model": ErrorResponse},
    },
    summary="To get all authors from the database with pagination.",
    tags=["Authors"],
)
async def get_all_authors(
    db_session: db_dependency,
    pager_params: pager_params_dependency,
) -> AuthorsList | ErrorResponse:
    authors = get_authors_with_offset_and_limit(
        db_session,
        offset=pager_params["skip"],
        limit=pager_params["limit"],
    )
    return authors


@router.put(
    "/authors/{author_id}",
    response_model=AuthorOut,
    responses={
        "401": {"model": ErrorResponse},
        "404": {"model": ErrorResponse},
        "500": {"model": ErrorResponse},
    },
    summary="To update an author based on the author id",
    tags=["Authors"],
)
async def update_author(
    db_session: db_dependency,
    author_in: AuthorIn,
    author_id: int = Path(..., title="Author ID", examples=[1]),
) -> AuthorOut | ErrorResponse:
    updated_author = update_author_on_db(db_session, author_id, author_in)
    return updated_author


@router.delete(
    "/authors/{author_id}",
    responses={
        "401": {"model": ErrorResponse},
        "403": {"model": ErrorResponse},
        "500": {"model": ErrorResponse},
    },
    status_code=HTTPResponseCode.NO_CONTENT,
    summary=(
        "To delete an author and a book based on the author ID,"
        "if the author's books are not available in stock."
    ),
    tags=["Authors"],
)
async def delete_author(
    db_session: db_dependency,
    author_id: int = Path(
        ...,
        title="Author ID",
        examples=[1],
    ),
) -> None:
    delete_author_on_db(db_session, author_id)
