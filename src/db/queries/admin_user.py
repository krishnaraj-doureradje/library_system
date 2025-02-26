from sqlmodel import select
from sqlmodel.sql._expression_select_cls import SelectOfScalar

from src.db.models.admin_user import AdminUser


def get_admin_user_stmt(user_id: str) -> SelectOfScalar[AdminUser]:
    """This function returns a select statement to get the admin user.

    Args:
        user_id (str): user_id

    Returns:
        SelectOfScalar[AdminUser]: Select statement for admin_user.
    """
    stmt = select(AdminUser).where(AdminUser.user_id == user_id)
    return stmt
