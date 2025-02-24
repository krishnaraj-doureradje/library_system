import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel

from src.db.engine import get_db_session, get_db_test_engine, get_db_test_session
from src.main import app
from src.utils.security import user_is_authenticated


@pytest.fixture(scope="session", autouse=True)
def setup_db() -> None:
    """Fixture to setup the database for testing."""
    SQLModel.metadata.create_all(get_db_test_engine())


def mock_user_is_authenticated():
    return None


@pytest.fixture(scope="session", autouse=True)
def client():  # type: ignore
    """Fixture to override the FastAPI app's dependency."""
    app.dependency_overrides[get_db_session] = get_db_test_session
    # Disable Basic authentication
    app.dependency_overrides[user_is_authenticated] = mock_user_is_authenticated

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
