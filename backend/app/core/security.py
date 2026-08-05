from typing import cast
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """
    Generate bcrypt hash of the plain-text password.
    """
    return cast(str, pwd_context.hash(password))


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against the saved bcrypt hash.
    """
    return cast(bool, pwd_context.verify(plain_password, hashed_password))

