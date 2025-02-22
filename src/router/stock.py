from fastapi import APIRouter, Depends, Path

from src.db.engine import db_dependency
from src.db.operation import create_stock_on_db, get_stock_book_out_from_db
from src.models.error_response import ErrorResponse
from src.models.http_response_code import HTTPResponseCode
from src.models.stock import StockIn, StockOut
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
