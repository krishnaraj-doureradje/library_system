from sqlalchemy import func
from sqlmodel import select
from sqlmodel.sql._expression_select_cls import SelectOfScalar

from src.db.models.user import User


def get_user_from_id_stmt(user_id: int) -> SelectOfScalar[User]:
    """This function returns a select statement to get the User.

    Args:
        user_id (int): The user id

    Returns:
        SelectOfScalar[User]: Select statement for user.
    """
    stmt = select(User).where(User.id == user_id)
    return stmt


def get_user_count_stmt() -> SelectOfScalar[int]:
    """This function returns a select statement to get the total number of users.

    Returns:
        SelectOfScalar[int]: Select statement for the count of user.
    """
    stmt = select(func.count().label("user_count")).select_from(User)
    return stmt


def get_users_stmt_with_limit_and_offset(*, offset: int, limit: int) -> SelectOfScalar[User]:
    """This function returns a select statement to get all users with pagination.

    Args:
        offset (int): Offset value.
        limit (int): Limit value.

    Returns:
        SelectOfScalar[User]: Select statement for all users.
    """
    stmt = select(User).limit(limit).offset(offset).order_by(User.id.asc())  # type: ignore
    return stmt
