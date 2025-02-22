from fastapi import APIRouter, Depends, Path

from src.db.engine import db_dependency
from src.db.operation import (
    create_book_on_db,
    get_book_out_from_db,
    get_books_with_offset_and_limit,
    update_book_on_db,
)
from src.helper.pagination import pager_params_dependency
from src.models.book import BookIn, BookOut, BooksList
from src.models.error_response import ErrorResponse
from src.models.http_response_code import HTTPResponseCode
from src.utils.security import user_is_authenticated

router = APIRouter(dependencies=[Depends(user_is_authenticated)])


@router.post(
    "/books",
    response_model=BookOut,
    responses={
        "401": {"model": ErrorResponse},
        "500": {"model": ErrorResponse},
    },
    summary="To create a new book.",
    tags=["Books"],
    status_code=HTTPResponseCode.CREATED,
)
async def create_book(
    db_session: db_dependency,
    book_in: BookIn,
) -> BookOut | ErrorResponse:
    new_book = create_book_on_db(db_session, book_in)
    return new_book


@router.get(
    "/books/{book_id}",
    response_model=BookOut,
    responses={
        "401": {"model": ErrorResponse},
        "404": {"model": ErrorResponse},
        "500": {"model": ErrorResponse},
    },
    summary="To get an book based on the book id.",
    tags=["Books"],
)
async def get_book(
    db_session: db_dependency,
    book_id: int = Path(
        ...,
        title="Book ID",
        examples=[1],
    ),
) -> BookOut | ErrorResponse:
    book_out = get_book_out_from_db(db_session, book_id)
    return book_out


@router.get(
    "/books",
    response_model=BooksList,
    responses={
        "401": {"model": ErrorResponse},
        "500": {"model": ErrorResponse},
    },
    summary="To get all books from the database with pagination.",
    tags=["Books"],
)
async def get_all_books(
    db_session: db_dependency,
    pager_params: pager_params_dependency,
) -> BooksList | ErrorResponse:
    books = get_books_with_offset_and_limit(
        db_session,
        offset=pager_params["skip"],
        limit=pager_params["limit"],
    )
    return books


@router.put(
    "/books/{book_id}",
    response_model=BookOut,
    responses={
        "401": {"model": ErrorResponse},
        "404": {"model": ErrorResponse},
        "500": {"model": ErrorResponse},
    },
    summary="To update an book based on the book id",
    tags=["Books"],
)
async def update_book(
    db_session: db_dependency,
    book_in: BookIn,
    book_id: int = Path(..., title="Book ID", examples=[1]),
) -> BookOut | ErrorResponse:
    updated_author = update_book_on_db(db_session, book_id, book_in)
    return updated_author


@router.delete(
    "/books/{book_id}",
    responses={
        "401": {"model": ErrorResponse},
        "500": {"model": ErrorResponse},
    },
    status_code=HTTPResponseCode.NO_CONTENT,
    summary="To delete a book based on the book id.",
    tags=["Books"],
)
async def delete_book(
    db_session: db_dependency,
    book_id: int = Path(
        ...,
        title="Book ID",
        examples=[1],
    ),
) -> None:
    raise NotImplementedError("Not implemented")
