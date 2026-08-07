from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

if TYPE_CHECKING:
    from app.models.user import User

from app.core.jwt import verify_access_token
from app.db.session import get_db
from app.repositories.auth import AuthRepository
from app.services.auth import AuthService

# Points to the login endpoint so Swagger UI knows where to obtain a token.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# Shared exception for all authentication failures.  Using a single,
# generic message avoids leaking whether a user account exists.
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_auth_repository(db: AsyncSession = Depends(get_db)) -> AuthRepository:
    """
    Dependency that provides an instance of AuthRepository.
    """
    return AuthRepository(db)


def get_auth_service(
    auth_repo: AuthRepository = Depends(get_auth_repository),
) -> AuthService:
    """
    Dependency that provides an instance of AuthService.
    """
    return AuthService(auth_repo)


def get_current_user_id(token: str = Depends(oauth2_scheme)) -> str:
    """
    FastAPI dependency that authenticates a request via Bearer JWT.

    Reads the ``Authorization: Bearer <token>`` header, verifies the token
    signature and expiry using :func:`~app.core.jwt.verify_access_token`, and
    returns the **subject** (user ID) embedded in the token.

    No database query is performed — this dependency is intentionally
    lightweight so it can be composed by higher-level dependencies that need
    to load or authorise a full user object.

    Args:
        token: Raw JWT extracted automatically by ``OAuth2PasswordBearer``.

    Returns:
        The ``sub`` claim from the verified token (a stringified user ID).

    Raises:
        HTTPException: 401 Unauthorized if the token is missing, expired,
            or otherwise invalid.
    """
    subject = verify_access_token(token)
    if subject is None:
        raise credentials_exception

    return subject


async def get_current_user(
    user_id: str = Depends(get_current_user_id),
    auth_repo: AuthRepository = Depends(get_auth_repository),
) -> "User":
    """
    FastAPI dependency that resolves a Bearer JWT into a full ``User`` model.

    Composes :func:`get_current_user_id` (which validates the token) with
    :meth:`AuthRepository.get_user_by_id` (which loads the row from the
    database).

    Args:
        user_id: The ``sub`` claim extracted from the verified JWT.
        auth_repo: Repository instance injected by FastAPI's DI container.

    Returns:
        The authenticated ``User`` ORM instance.

    Raises:
        HTTPException: 401 Unauthorized if the token is valid but the user
            no longer exists in the database.
    """
    user = await auth_repo.get_user_by_id(user_id)
    if user is None:
        raise credentials_exception
    return user
