import logging
from typing import Sequence, TypeVar

from sqlalchemy import Delete, Update
from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError
from sqlmodel import SQLModel
from sqlmodel.sql._expression_select_cls import SelectOfScalar

from src.db.engine import db_dependency
from src.exceptions.app import SqlException
from src.exceptions.db import handle_db_exception
from src.models.http_response_code import HTTPResponseCode

logger = logging.getLogger("sql")
T = TypeVar("T", bound=SQLModel)


def execute_all_query(
    db_session: db_dependency,
    sql_models: Sequence[T],
    *,
    is_commit: bool = True,
    is_refresh_after_commit: bool = False,
) -> None:
    """
    Adds multiple SQLModel instances to the session, commits the transaction,and optionally refreshes the models
    to get their updated state.
    This method is used for executing insert and update queries.

    Args:
        db_session (db_dependency): The database session to use for executing the query.
        sql_models (Sequence[T]): A sequence of SQLModel instances to be added to the session.
        is_commit (bool, optional): Whether to commit the transaction after adding the models. Defaults to True.
        is_refresh_after_commit (bool, optional): Whether to refresh the models after committing the transaction. Defaults to False.

    Raises:
        SqlException: Raised when a database error occurs, with details logged.
    """  # noqa: E501
    try:
        db_session.add_all(sql_models)
        if is_commit:
            db_session.commit()

        if is_commit and is_refresh_after_commit:
            for sql_model in sql_models:
                db_session.refresh(sql_model)

    except (IntegrityError, OperationalError, SQLAlchemyError) as exc:
        handle_db_exception(db_session, exc)


def fetch_one_or_none(db_session: db_dependency, stmt: SelectOfScalar[T]) -> T | None:
    """
    Fetch a single record from the database based on the given condition.

    Args:
        db_session (db_dependency): The database session to use for querying.
        stmt (SelectOfScalar[T]): The SQL statement for selecting a single record.

    Returns:
        T | None: The first matching record as an instance of SQLModel, or None if no match is found.

    Raises:
        SqlException: Raised when a database error occurs.
    """  # noqa: E501
    try:
        result = db_session.exec(stmt).one_or_none()
        return result
    except SQLAlchemyError as exc:
        logger.error(f"Database error while fetching one record: {exc}")
        raise SqlException(
            status_code=HTTPResponseCode.INTERNAL_SERVER_ERROR, message=str(exc)
        ) from None


def fetch_all(db_session: db_dependency, stmt: SelectOfScalar[T]) -> Sequence[T]:
    """
    Fetch all records from the database based on the given condition.

    Args:
        db_session (db_dependency): The database session to use for querying.
        stmt (SelectOfScalar[T]): The SQL statement for selecting all records.

    Returns:
        Sequence[T]: All matching records as instances of SQLModel.

    Raises:
        SqlException: Raised when a database error occurs.
    """
    try:
        result = db_session.exec(stmt).fetchall()
        return result
    except SQLAlchemyError as exc:
        logger.error(f"Database error while fetching all records: {exc}")
        raise SqlException(
            status_code=HTTPResponseCode.INTERNAL_SERVER_ERROR, message=str(exc)
        ) from None


def delete_all_query(
    db_session: db_dependency,
    sql_models: Sequence[T],
    *,
    is_commit: bool = True,
) -> None:
    """Deletes all records from the database based on the given models.

    Args:
        db_session (db_dependency): The database session to use for executing the query.
        sql_models (Sequence[T]): A sequence of SQLModel instances to be deleted
                                  from the session.
        is_commit (bool, optional): Whether to commit the transaction after deleting
                                    the records. Defaults to True.

    Raises:
        SqlException: Raised when a database error occurs.
    """
    try:
        for sql_model in sql_models:
            db_session.delete(sql_model)
        if is_commit:
            db_session.commit()

    except (IntegrityError, OperationalError, SQLAlchemyError) as exc:
        handle_db_exception(db_session, exc)


def execute_statement(
    db_session: db_dependency,
    stmt: Delete | Update,
    *,
    is_commit: bool = True,
) -> None:
    """Executes a Delete or Update statement in the database.

    Args:
        db_session (db_dependency): The database session to use for executing the query.
        stmt (Delete | Update): The SQLAlchemy Delete or Update statement to execute.
        is_commit (bool, optional): Whether to commit the transaction after executing
                                    the statement. Defaults to True.

    Raises:
        SqlException: Raised when a database error occurs.
    """
    try:
        db_session.exec(stmt)  # type: ignore

        if is_commit:
            db_session.commit()

    except (IntegrityError, OperationalError, SQLAlchemyError) as exc:
        handle_db_exception(db_session, exc)
