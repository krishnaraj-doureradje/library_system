from fastapi import APIRouter, Depends, Path

from src.db.engine import db_dependency
from src.db.operation import (
    add_new_quantity_to_the_existing_stocks_on_db,
    create_stock_on_db,
    get_stock_book_out_from_db,
    get_stocks_with_offset_and_limit,
)
from src.helper.pagination import pager_params_dependency
from src.models.error_response import ErrorResponse
from src.models.http_response_code import HTTPResponseCode
from src.models.stock import StockIn, StockOut, StockQuantityAdd, StocksList
from src.utils.security import user_is_authenticated

router = APIRouter(dependencies=[Depends(user_is_authenticated)])


@router.post(
    "/stocks",
    response_model=StockOut,
    responses={
        "401": {"model": ErrorResponse},
        "500": {"model": ErrorResponse},
    },
    summary="To create a book stock in the system.",
    tags=["Stocks"],
    status_code=HTTPResponseCode.CREATED,
)
async def create_stock(
    db_session: db_dependency,
    stock_in: StockIn,
) -> StockOut | ErrorResponse:
    new_stock = create_stock_on_db(db_session, stock_in)
    return new_stock


@router.get(
    "/stocks/{book_id}",
    response_model=StockOut,
    responses={
        "401": {"model": ErrorResponse},
        "404": {"model": ErrorResponse},
        "500": {"model": ErrorResponse},
    },
    summary="To get a stock based on the book id.",
    tags=["Stocks"],
)
async def get_stock(
    db_session: db_dependency,
    book_id: int = Path(
        ...,
        title="Book ID",
        examples=[1],
    ),
) -> StockOut | ErrorResponse:
    stock_out = get_stock_book_out_from_db(db_session, book_id)
    return stock_out


@router.get(
    "/stocks",
    response_model=StocksList,
    responses={
        "401": {"model": ErrorResponse},
        "500": {"model": ErrorResponse},
    },
    summary="To get all stocks from the database with pagination.",
    tags=["Stocks"],
)
async def get_all_stocks(
    db_session: db_dependency,
    pager_params: pager_params_dependency,
) -> StocksList | ErrorResponse:
    stocks = get_stocks_with_offset_and_limit(
        db_session,
        offset=pager_params["skip"],
        limit=pager_params["limit"],
    )
    return stocks


@router.put(
    "/stocks/{book_id}",
    response_model=StockOut,
    responses={
        "401": {"model": ErrorResponse},
        "404": {"model": ErrorResponse},
        "500": {"model": ErrorResponse},
    },
    summary="To add new quantity to the existing stocks",
    tags=["Stocks"],
)
async def update_stocks(
    db_session: db_dependency,
    stock_quantity: StockQuantityAdd,
    book_id: int = Path(..., title="Book ID", examples=[1]),
) -> StockOut | ErrorResponse:
    updated_stock = add_new_quantity_to_the_existing_stocks_on_db(
        db_session, book_id, stock_quantity
    )
    return updated_stock
