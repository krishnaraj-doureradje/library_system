import hashlib
import secrets
from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from src.config.config import APP_CONFIG
from src.constants.security import PASSWORD_MIN_LEN
from src.db.engine import db_dependency
from src.db.operations.admin_user import get_admin_user
from src.exceptions.app import AuthenticationException
from src.models.http_response_code import HTTPResponseCode

security = HTTPBasic()


def hash_password(password: str) -> str:
    """Hash a plain-text password securely using hashlib.

    Args:
        password (str): Plain-text password (must not be empty)

    Returns:
        str: Securely hashed password

    Raises:
        ValueError: If the password is empty or too short
    """
    if not password or len(password) < PASSWORD_MIN_LEN:
        raise ValueError("Password must be at least 8 characters long")

    sha256_hash = hashlib.sha256()
    sha256_hash.update(password.encode("utf-8"))
    return sha256_hash.hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify if a plain-text password matches its hashed version.

     Args:
        plain_password (str): The user-provided password in plain text.
        hashed_password (str): The securely stored hashed password.

    Returns:
        bool: True if the plain-text password matches the hash, False otherwise.
    """
    return hash_password(plain_password) == hashed_password


def user_is_authenticated(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)], db_session: db_dependency
) -> None:
    """The method is used to valid the authentication

    Args:
        credentials (Annotated[HTTPBasicCredentials, Depends): Basic credentials
        db_session (db_dependency): Database session.

    Raises:
        AuthenticationException: Raise exception if it's not a valid username or password
    """
    if not APP_CONFIG["authentication"]["basic"]["enable"]:
        return None

    username = credentials.username
    password = credentials.password

    admin_user = get_admin_user(db_session, username)

    if admin_user is None:
        raise AuthenticationException(
            status_code=HTTPResponseCode.UNAUTHORIZED,
            message="Incorrect username or password",
        )

    is_correct_username = secrets.compare_digest(username, admin_user.user_id)
    is_correct_password = verify_password(password, admin_user.password)

    if not (is_correct_username and is_correct_password):
        raise AuthenticationException(
            status_code=HTTPResponseCode.UNAUTHORIZED,
            message="Incorrect username or password",
        )
