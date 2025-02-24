import logging

from src.db.engine import db_dependency
from src.exceptions.app import SqlException
from src.models.http_response_code import HTTPResponseCode

logger = logging.getLogger("sql")


def handle_db_exception(db_session: db_dependency, exc: Exception) -> None:
    """Handles database exceptions by rolling back and logging the error.

    Args:
        db_session (db_dependency): The database session to use for executing the query.
        exc (Exception): SQlalchemy Exception

    Raises:
        SqlException: Raise SqlException
    """
    db_session.rollback()
    error_type = exc.__class__.__name__
    logger.error(f"{error_type} occurred: {exc}")
    raise SqlException(
        status_code=HTTPResponseCode.INTERNAL_SERVER_ERROR, message=str(exc)
    ) from None
