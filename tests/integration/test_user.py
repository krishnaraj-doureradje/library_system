from typing import Any

from fastapi.testclient import TestClient

from src.exceptions.app import NotFoundException, SqlException
from src.models.http_response_code import HTTPResponseCode
from tests.integration.constant import COUNT_ZERO

user: dict[str, Any] = {"email": "john.doe@example.com", "first_name": "John", "last_name": "Doe"}


def test_users_with_count_zero(client: TestClient) -> None:
    """Test the users details endpoint."""
    response = client.get("/users")
    assert response.status_code == HTTPResponseCode.OK
    response_json = response.json()
    assert len(response_json["users"]) == COUNT_ZERO


def test_user_with_id_fail(client: TestClient) -> None:
    """Test the user with id details endpoint."""
    response = client.get("/user/1")
    assert response.status_code == HTTPResponseCode.NOT_FOUND


def test_add_users(client: TestClient) -> None:
    """Test to add users."""

    for i in range(1, 6):
        user_copy = user.copy()
        user_copy["email"] = f"{str(i) + '_'}{user_copy['email']}"
        user_copy["first_name"] = f"{user_copy['first_name'] + '_' + str(i)}"
        user_copy["last_name"] = f"{user_copy['last_name'] + '_' + str(i)}"

        user_responses = client.post("/users", json=user_copy)
        assert user_responses.status_code == HTTPResponseCode.CREATED


def test_add_user_fail(client: TestClient) -> None:
    """Test to add the same user's email."""
    try:
        client.post("/users", json=user)
    except SqlException as exc:
        assert exc.status_code == HTTPResponseCode.INTERNAL_SERVER_ERROR


def test_user_with_id_pass(client: TestClient) -> None:
    """Test the user with id details endpoint."""
    response = client.get("/users/1")
    assert response.status_code == HTTPResponseCode.OK


def test_book_users_endpoint_fail(client: TestClient) -> None:
    """Test the user's update endpoint."""
    # Test Fail scenario
    try:
        client.put("/users/33", json=user)
    except NotFoundException as exc:
        assert exc.status_code == HTTPResponseCode.NOT_FOUND

    # Update scenario
    user_copy = user.copy()
    user_copy["email"] = "user1@test.fr"
    response = client.put("/users/1", json=user_copy)
    assert response.status_code == HTTPResponseCode.OK
