import os
from pathlib import Path
from typing import Iterator

import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlmodel import text

from src.config.config import APP_CONFIG
from src.db.check import db_settings_initializations
from src.db.engine import get_db_session, get_db_test_session
from src.main import app
from src.utils.security import user_is_authenticated


def get_alembic_path() -> str:
    """Get alembic file path"""
    current_dir = Path(__file__).parent
    parent_dir = current_dir.parent
    alembic_ini_path = os.path.join(parent_dir, "alembic.ini")
    if not os.path.exists(alembic_ini_path):
        raise FileExistsError(f"Alembic file does not exist: {alembic_ini_path}")

    return alembic_ini_path


@pytest.fixture(scope="session", autouse=True)
def setup_db() -> Iterator:  # type: ignore
    """Fixture to setup the database for testing."""
    remove_test_db_file()

    alembic_path = get_alembic_path()
    alembic_cfg = Config(alembic_path)
    alembic_cfg.set_main_option(
        "sqlalchemy.url",
        f"sqlite:///{APP_CONFIG['testing_db']['file']}",
    )
    command.upgrade(alembic_cfg, "head")
    db_settings_initializations()
    delete_data_from_tables()
    yield
    # command.downgrade(alembic_cfg, "base")
    remove_test_db_file()


def remove_test_db_file() -> None:
    """Remove test db file."""
    if os.path.exists(APP_CONFIG["testing_db"]["file"]):
        os.remove(APP_CONFIG["testing_db"]["file"])


def delete_data_from_tables() -> None:
    """Delete the data."""
    session = next(get_db_test_session())
    session.execute(text("DELETE FROM reservations;"))
    session.execute(text("DELETE FROM users;"))
    session.execute(text("DELETE FROM stocks;"))
    session.execute(text("DELETE FROM books;"))
    session.execute(text("DELETE FROM authors;"))
    session.commit()
    session.close()


def mock_user_is_authenticated() -> None:
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
