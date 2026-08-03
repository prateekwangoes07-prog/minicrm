from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.repositories.user import UserRepository
from app.services.user import UserService


def get_user_repository(db: AsyncSession = Depends(get_db)) -> UserRepository:
    """
    Dependency that provides an instance of UserRepository.
    """
    return UserRepository(db)


def get_user_service(
    user_repo: UserRepository = Depends(get_user_repository),
) -> UserService:
    """
    Dependency that provides an instance of UserService.
    """
    return UserService(user_repo)
