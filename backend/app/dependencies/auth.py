from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.jwt import verify_access_token
from app.db.session import get_db
from app.repositories.auth import AuthRepository
from app.services.auth import AuthService

# Points to the login endpoint so Swagger UI knows where to obtain a token.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


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
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    subject = verify_access_token(token)
    if subject is None:
        raise credentials_exception

    return subject
