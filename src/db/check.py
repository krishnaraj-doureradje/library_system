import logging
from contextlib import contextmanager

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text

from src.db.engine import get_db_session

logger = logging.getLogger("app")


def check_db_exist() -> None:
    """Check if the database connection is valid and accessible."""
    try:
        with contextmanager(get_db_session)() as session:
            session.exec(text("SELECT 1"))  # type: ignore
            logger.info("Database connection verified successfully.")
    except SQLAlchemyError as e:
        logger.error(f"Failed to verify database connection: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error while verifying database connection: {str(e)}")
        raise
