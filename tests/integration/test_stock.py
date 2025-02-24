from typing import Any

from fastapi.testclient import TestClient

from src.exceptions.app import NotFoundException, SqlException
from src.models.http_response_code import HTTPResponseCode
from tests.integration.constant import COUNT_ZERO

stock: dict[str, Any] = {"book_id": 1, "stock_quantity": 1}


def test_stocks_with_count_zero(client: TestClient) -> None:
    """Test the stock details endpoint."""
    response = client.get("/stocks")
    assert response.status_code == HTTPResponseCode.OK
    response_json = response.json()
    assert len(response_json["stocks"]) == COUNT_ZERO


def test_stock_with_id_fail(client: TestClient) -> None:
    """Test the stock with id details endpoint."""
    response = client.get("/stock/1")
    assert response.status_code == HTTPResponseCode.NOT_FOUND


def test_add_stocks(client: TestClient) -> None:
    """Test to add the book to the stocks."""
    book_responses = client.get("/books")
    assert book_responses.status_code == HTTPResponseCode.OK

    book_responses_json = book_responses.json()
    for book in book_responses_json["books"]:
        stock: dict[str, Any] = {"book_id": book["id"], "stock_quantity": 10}
        stock_response = client.post("/stocks", json=stock)
        assert stock_response.status_code == HTTPResponseCode.CREATED


def test_add_stock_fail(client: TestClient) -> None:
    """Test to add the book to the stocks."""
    stock: dict[str, Any] = {"book_id": 1, "stock_quantity": 10}
    try:
        client.post("/stocks", json=stock)
    except SqlException as exc:
        assert exc.status_code == HTTPResponseCode.INTERNAL_SERVER_ERROR


def test_stock_with_id_pass(client: TestClient) -> None:
    """Test the stock with id details endpoint."""
    response = client.get("/stocks/1")
    assert response.status_code == HTTPResponseCode.OK


def test_book_stocks_endpoint_fail(client: TestClient) -> None:
    """Test the stock's update endpoint."""
    # Test Fail scenario
    try:
        client.put("/books/33", json=stock)
    except NotFoundException as exc:
        assert exc.status_code == HTTPResponseCode.NOT_FOUND

    # Update scenario
    response = client.put("/stocks/1", json=stock)
    assert response.status_code == HTTPResponseCode.OK

    response_json = response.json()
    assert response_json["stock_quantity"] == 11  # noqa: PLR2004
