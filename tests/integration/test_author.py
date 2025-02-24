from typing import Any

from constant import COUNT_ONE, COUNT_TWO, COUNT_ZERO
from fastapi.testclient import TestClient

from src.exceptions.app import NotFoundException, SqlException
from src.models.http_response_code import HTTPResponseCode

author: dict[str, Any] = {
    "birth_date": "1980-05-15",
    "first_name": "John",
    "last_name": "Doe",
    "nationality": "USA",
}


def test_authors_with_count_zero(client: TestClient) -> None:
    """Test the authors details endpoint."""
    response = client.get("/authors")
    assert response.status_code == HTTPResponseCode.OK
    response_json = response.json()
    assert len(response_json["authors"]) == COUNT_ZERO


def test_author_with_id_fail(client: TestClient) -> None:
    """Test the author with id details endpoint."""
    response = client.get("/author/1")
    assert response.status_code == HTTPResponseCode.NOT_FOUND


def test_create_authors(client: TestClient) -> None:
    """Test creation of author endpoint."""
    response = client.post("/authors", json=author)
    assert response.status_code == HTTPResponseCode.CREATED

    # Add second author
    author_copy = author.copy()
    author_copy["first_name"] = "Krishnaraj"

    response = client.post("/authors", json=author_copy)
    assert response.status_code == HTTPResponseCode.CREATED


def test_create_author_fail(client: TestClient) -> None:
    """Test creation of authors endpoint."""
    try:
        client.post("/authors", json=author)
    except SqlException as exc:
        assert exc.status_code == HTTPResponseCode.INTERNAL_SERVER_ERROR


def test_author_with_id_pass(client: TestClient) -> None:
    """Test the author with id details endpoint."""
    response = client.get("/authors/2")
    assert response.status_code == HTTPResponseCode.OK

    response_json = response.json()
    assert response_json["id"] == COUNT_TWO
    assert response_json["first_name"] == "Krishnaraj"


def test_author_update_endpoint(client: TestClient) -> None:
    """Test the author's update endpoint."""
    # Test Fail scenario
    try:
        client.put("/authors/3", json=author)
    except NotFoundException as exc:
        assert exc.status_code == HTTPResponseCode.NOT_FOUND

    # Update scenario
    author_copy = author.copy()
    author_copy["last_name"] = "Doureradje"
    author_copy["first_name"] = "Krishnaraj"
    response = client.put("/authors/1", json=author)
    assert response.status_code == HTTPResponseCode.OK


def test_author_delete_endpoint(client: TestClient) -> None:  # noqa: PLR0915
    """Test the author's delete endpoint."""
    # Even if author id 22 is not present in the database, the response will be 204.
    response = client.delete("/authors/22")
    assert response.status_code == HTTPResponseCode.NO_CONTENT

    # Delete id present in the DB
    response = client.delete("/authors/2")
    assert response.status_code == HTTPResponseCode.NO_CONTENT

    # Verification
    response = client.get("/authors")
    assert response.status_code == HTTPResponseCode.OK
    response_json = response.json()
    assert len(response_json["authors"]) == COUNT_ONE

    # Verification with ID
    try:
        client.get("/authors/2")
    except NotFoundException as exc:
        assert exc.status_code == HTTPResponseCode.NOT_FOUND
