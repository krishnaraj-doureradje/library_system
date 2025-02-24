from typing import Any

from fastapi.testclient import TestClient

from src.exceptions.app import NotFoundException, ReservationException, SqlException
from src.models.http_response_code import HTTPResponseCode
from tests.integration.constant import COUNT_ONE, COUNT_ZERO

reservation: dict[str, Any] = {"book_id": 1, "user_id": 1}


def test_reservation_with_count_zero(client: TestClient) -> None:
    """Test the reservations details endpoint."""
    response = client.get("/reservations")
    assert response.status_code == HTTPResponseCode.OK
    response_json = response.json()
    assert len(response_json["reservations"]) == COUNT_ZERO


def test_reservation_with_id_fail(client: TestClient) -> None:
    """Test the reservation with id details endpoint."""
    try:
        client.get("/reservations/1")
    except NotFoundException as exc:
        assert exc.status_code == HTTPResponseCode.NOT_FOUND


def test_add_reservation(client: TestClient) -> None:
    """Test the reservation with id details endpoint."""
    response = client.post("/reservations", json=reservation)
    assert response.status_code == HTTPResponseCode.CREATED


def test_add_reservation_fail(client: TestClient) -> None:
    """Test the reservation with id details endpoint."""
    try:
        client.post("/reservations", json=reservation)
    except ReservationException as exc:
        assert exc.status_code == HTTPResponseCode.BAD_REQUEST


def test_get_reservations(client: TestClient) -> None:
    """Test the reservations details endpoint."""
    response = client.get("/reservations")
    assert response.status_code == HTTPResponseCode.OK
    response_json = response.json()
    assert len(response_json["reservations"]) == COUNT_ONE

    response = client.get("/reservations/1")
    assert response.status_code == HTTPResponseCode.OK
    response_json = response.json()
    assert response_json["id"] == 1
    assert response_json["book_id"] == reservation["book_id"]
    assert response_json["user_id"] == reservation["user_id"]


def test_update_reservations(client: TestClient) -> None:
    """Test the update reservations details endpoint."""

    response = client.put("/reservations/1", json=reservation)
    assert response.status_code == HTTPResponseCode.OK
    # Test returned book case
    try:
        client.put("/reservations/1", json=reservation)
    except ReservationException as exp:
        assert exp.status_code == HTTPResponseCode.BAD_REQUEST


def test_user_case_verification(client: TestClient) -> None:  # noqa: PLR0915
    """Application use case verification"""

    # Could not delete author if the author's book in stocks
    try:
        client.delete("/authors/1")
    except SqlException as exc:
        assert exc.status_code == HTTPResponseCode.FORBIDDEN
    # Same for the book
    try:
        client.delete("/books/1")
    except SqlException as exc:
        assert exc.status_code == HTTPResponseCode.FORBIDDEN

    # Create an author and book
    author_response = client.post(
        "/authors",
        json={
            "birth_date": "1988-05-15",
            "first_name": "John",
            "last_name": "Doe",
            "nationality": "USA",
        },
    )
    assert author_response.status_code == HTTPResponseCode.CREATED

    book_response = client.post(
        "/books",
        json={
            "author_id": 1,
            "category": "Science fiction part1",
            "published_date": "1985-05-15",
            "title": "Pride and Prejudice",
        },
    )
    assert book_response.status_code == HTTPResponseCode.CREATED

    author_id = author_response.json()["id"]
    book_id = book_response.json()["id"]
    # Deleting the author implicitly deletes the author and the book
    author_delete_response = client.delete(
        f"/authors/{author_id}",
    )
    assert author_delete_response.status_code == HTTPResponseCode.NO_CONTENT

    try:
        client.get(f"/authors/{author_id}")
    except NotFoundException as exc:
        assert exc.status_code == HTTPResponseCode.NOT_FOUND

    try:
        client.get(f"/books/{book_id}")
    except NotFoundException as exc:
        assert exc.status_code == HTTPResponseCode.NOT_FOUND
