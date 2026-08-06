from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.repositories.auth import AuthRepository
from app.services.auth import AuthService


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
