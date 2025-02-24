from src.db.engine import db_dependency
from src.db.execution import fetch_one_or_none
from src.db.models.admin_user import AdminUser
from src.db.query import (
    get_admin_user_stmt,
)


def get_admin_user(db_session: db_dependency, user_id: str) -> AdminUser | None:
    """Retrieve an admin user from the database.

    Args:
        db_session (db_dependency): Databases sessions.
        user_id (str): Admin user_id

    Returns:
        AdminUser | None: The corresponding AdminUser object if found, otherwise None.
    """
    admin_user_stmt = get_admin_user_stmt(user_id)
    admin_user = fetch_one_or_none(db_session, admin_user_stmt)
    return admin_user
