import pytest

from src.constants.security import PASSWORD_MIN_LEN
from src.utils.security import hash_password, verify_password


def test_hash_password_valid() -> None:
    """Valid password"""
    password = "validpassword123"
    hashed = hash_password(password)
    assert isinstance(hashed, str)
    assert len(hashed) == 64  # SHA-256 produces a 64-character hexadecimal string  # noqa: PLR2004


def test_hash_password_empty() -> None:
    """Fail password scenario"""
    with pytest.raises(ValueError, match="Password must be at least 8 characters long"):
        hash_password("")
        hash_password("short")


def test_hash_password_minimum_length() -> None:
    """Valid password length"""
    password = "a" * PASSWORD_MIN_LEN
    hashed = hash_password(password)
    assert isinstance(hashed, str)
    assert len(hashed) == 64  # noqa: PLR2004


def test_hash_password_consistency() -> None:
    """Check password consistency"""
    password = "testpassword123"
    hash1 = hash_password(password)
    hash2 = hash_password(password)
    assert hash1 == hash2


def test_verify_password_correct() -> None:
    """Verify password is valid"""
    password = "correctpassword123"
    hashed = hash_password(password)
    assert verify_password(password, hashed) is True


def test_verify_password_incorrect() -> None:
    """Incorrect password verification"""
    correct_password = "correctpassword123"
    incorrect_password = "incorrectpassword123"
    hashed = hash_password(correct_password)
    assert verify_password(incorrect_password, hashed) is False


def test_verify_password_empty() -> None:
    """Empty Password verification"""
    hashed = hash_password("somepassword")
    with pytest.raises(ValueError, match="Password must be at least 8 characters long"):
        verify_password("", hashed)


def test_verify_password_too_short() -> None:
    """Check not a valid password"""
    hashed = hash_password("somepassword")
    with pytest.raises(ValueError, match="Password must be at least 8 characters long"):
        verify_password("short", hashed)
