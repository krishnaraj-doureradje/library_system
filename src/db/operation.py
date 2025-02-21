from src.db.engine import db_dependency
from src.db.execution import execute_all_query, fetch_one_or_none
from src.db.models.admin_user import AdminUser
from src.db.models.author import Author
from src.db.query import get_admin_user_stmt
from src.models.author import AuthorIn, AuthorOut


def create_author_on_db(db_session: db_dependency, author_in: AuthorIn) -> AuthorOut:
    """Create a new author in the databases

    Args:
        db_session (db_dependency): Database session.
        author_in (AuthorIn): Author details

    Returns:
        AuthorOut: Author details with ID
    """
    new_author = Author(**author_in.model_dump())
    # Refresh the object after commit to get the primary key
    execute_all_query(db_session, [new_author], is_commit=True, is_refresh_after_commit=True)
    return AuthorOut(**new_author.model_dump())


def get_admin_user(db_session: db_dependency, user_id: str) -> AdminUser | None:
    admin_user_stmt = get_admin_user_stmt(user_id)
    admin_user = fetch_one_or_none(db_session, admin_user_stmt)
    return admin_user
