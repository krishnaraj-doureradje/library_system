from fastapi.testclient import TestClient

from src.models.http_response_code import HTTPResponseCode


def test_health_check(client: TestClient) -> None:
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == HTTPResponseCode.OK
    assert response.json() == {"status": "ok"}
