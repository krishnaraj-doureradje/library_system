from src.db.engine import db_dependency
from src.db.execution import execute_all_query, fetch_all, fetch_one_or_none
from src.db.models.user import User
from src.db.query import (
    get_user_count_stmt,
    get_user_from_id_stmt,
    get_users_stmt_with_limit_and_offset,
)
from src.exceptions.app import NotFoundException
from src.helper.pagination import pagination_details
from src.models.http_response_code import HTTPResponseCode
from src.models.user import UserIn, UserOut, UsersList


def create_user_on_db(db_session: db_dependency, user_in: UserIn) -> UserOut:
    """Create a new user in the databases

    Args:
        db_session (db_dependency): Database session.
        user_in (UserIn): User details

    Returns:
        UserOut: User details with ID
    """
    new_user = User(**user_in.model_dump())
    # Refresh the object after commit to get the primary key
    execute_all_query(db_session, [new_user], is_commit=True, is_refresh_after_commit=True)
    return UserOut(**new_user.model_dump())


def get_user_from_id(db_session: db_dependency, user_id: int) -> User:
    """Get an user based on the user id.

    Args:
        db_session (db_dependency):  Database session.
        user_id (int): User id

    Raises:
        NotFoundException: Raised when the user id is not found in the database.

    Returns:
        User: User details
    """
    user_stmt = get_user_from_id_stmt(user_id)
    user = fetch_one_or_none(db_session, user_stmt)

    if user is None:
        raise NotFoundException(
            status_code=HTTPResponseCode.NOT_FOUND,
            message=f"{user_id=} not found in the database",
        )

    return user


def get_user_out_from_db(db_session: db_dependency, user_id: int) -> UserOut:
    """Get userOut model response.

    Args:
        db_session (db_dependency): Database session.
        user_id (int): User id.

    Returns:
        UserOut: User details.
    """
    db_user = get_user_from_id(db_session, user_id)
    return UserOut(**db_user.model_dump())


def get_users_with_offset_and_limit(
    db_session: db_dependency, *, offset: int, limit: int
) -> UsersList:
    """Get all users with pagination.

    Args:
        db_session (db_dependency): Database session.
        offset (int): Offset value.
        limit (int): Limit value.

    Returns:
        UsersList: List of authors.
    """
    users_count_stmt = get_user_count_stmt()
    users_count = fetch_one_or_none(db_session, users_count_stmt)  # type: ignore

    # There is nothing to fetch if the authors_count is None
    if users_count is None:
        return UsersList(
            users=[],
            number_of_users=0,
            number_of_pages=0,
            current_page=0,
            next_page=None,
            previous_page=None,
        )

    users_stmt = get_users_stmt_with_limit_and_offset(offset=offset, limit=limit)
    users = [UserOut(**user.model_dump()) for user in fetch_all(db_session, users_stmt)]

    # Calculate the number of pages, current page, next page, and previous page
    number_of_pages, current_page, next_page, previous_page = pagination_details(
        offset=offset, limit=limit, counts=users_count
    )

    return UsersList(
        users=users,
        number_of_users=users_count,
        number_of_pages=number_of_pages,
        current_page=current_page,
        next_page=next_page,
        previous_page=previous_page,
    )


def update_user_on_db(db_session: db_dependency, user_id: int, user_in: UserIn) -> UserOut:
    """Update an user based on the user id.

    Args:
        db_session (db_dependency): Database session.
        user_id (int): User id.
        user_in (UserIn): User details.

    Raises:
        NotFoundException: Raised when the user id is not found in the database.

    Returns:
        UserOut: Updated user details.
    """
    db_user = get_user_from_id(db_session, user_id)

    # Update the author fields with the new values
    for field, value in user_in.model_dump().items():
        setattr(db_user, field, value)

    user_out = UserOut(**db_user.model_dump())
    # We don't need to refresh the object for the update operation, so we can avoid
    # making a select request to the database.
    execute_all_query(
        db_session,
        [db_user],  # type: ignore
    )
    return user_out
