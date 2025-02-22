import logging
from contextlib import contextmanager

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text

from src.db.engine import get_db_session

logger = logging.getLogger("app")


def db_settings_initializations() -> None:
    """Databases settings initializations."""
    try:
        with contextmanager(get_db_session)() as session:
            session.exec(text("PRAGMA foreign_keys = ON;"))  # type: ignore
            logger.info("Database connection verified successfully.")
    except SQLAlchemyError as e:
        logger.error(f"Failed to verify database connection: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error while verifying database connection: {str(e)}")
        raise
