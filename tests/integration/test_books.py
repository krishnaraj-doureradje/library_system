from typing import Any

from fastapi.testclient import TestClient

from src.exceptions.app import NotFoundException, SqlException
from src.models.http_response_code import HTTPResponseCode
from tests.integration.constant import COUNT_ONE, COUNT_TWO, COUNT_ZERO

book: dict[str, Any] = {
    "author_id": 1,
    "category": "Science fiction",
    "published_date": "1980-05-15",
    "title": "Pride and Prejudice",
}


def test_books_with_count_zero(client: TestClient) -> None:
    """Test the book details endpoint."""
    response = client.get("/books")
    assert response.status_code == HTTPResponseCode.OK
    response_json = response.json()
    assert len(response_json["books"]) == COUNT_ZERO


def test_book_with_id_fail(client: TestClient) -> None:
    """Test the book with id details endpoint."""
    try:
        client.get("/books/1")
    except NotFoundException as exc:
        assert exc.status_code == HTTPResponseCode.NOT_FOUND


def test_create_books(client: TestClient) -> None:
    """Test creation of book endpoint."""
    response = client.post("/books", json=book)
    assert response.status_code == HTTPResponseCode.CREATED

    # Add second book
    book_copy = book.copy()
    book_copy["title"] = "Pride and Prejudice Part 1"
    book_copy["category"] = "Science fictions"

    response = client.post("/books", json=book_copy)
    assert response.status_code == HTTPResponseCode.CREATED


def test_create_book_fail(client: TestClient) -> None:
    """Test creation of book endpoint."""
    try:
        client.post("/books", json=book)
    except SqlException as exc:
        assert exc.status_code == HTTPResponseCode.INTERNAL_SERVER_ERROR


def test_book_with_id_pass(client: TestClient) -> None:
    """Test the book with id details endpoint."""
    response = client.get("/books/2")
    assert response.status_code == HTTPResponseCode.OK

    response_json = response.json()
    assert response_json["id"] == COUNT_TWO


def test_book_update_endpoint_fail(client: TestClient) -> None:
    """Test the book's update endpoint."""
    # Test Fail scenario
    try:
        client.put("/books/3", json=book)
    except NotFoundException as exc:
        assert exc.status_code == HTTPResponseCode.NOT_FOUND

    # Update scenario
    book_copy = book.copy()
    book_copy["category"] = "Detective"
    response = client.put("/books/1", json=book_copy)
    assert response.status_code == HTTPResponseCode.OK


def test_book_delete_endpoint(client: TestClient) -> None:  # noqa: PLR0915
    """Test the book's delete endpoint."""
    # Even if book id 22 is not present in the database, the response will be 204.
    response = client.delete("/books/22")
    assert response.status_code == HTTPResponseCode.NO_CONTENT

    # Delete id present in the DB
    response = client.delete("/books/2")
    assert response.status_code == HTTPResponseCode.NO_CONTENT

    # Verification
    response = client.get("/books")
    assert response.status_code == HTTPResponseCode.OK
    response_json = response.json()
    assert len(response_json["books"]) == COUNT_ONE

    # Verification with ID
    try:
        client.get("/books/2")
    except NotFoundException as exc:
        assert exc.status_code == HTTPResponseCode.NOT_FOUND
