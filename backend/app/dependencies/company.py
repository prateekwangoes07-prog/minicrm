from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.repositories.company import CompanyRepository
from app.services.company import CompanyService


def get_company_repository(db: AsyncSession = Depends(get_db)) -> CompanyRepository:
    """
    Dependency that provides an instance of CompanyRepository.
    """
    return CompanyRepository(db)


def get_company_service(
    company_repo: CompanyRepository = Depends(get_company_repository),
) -> CompanyService:
    """
    Dependency that provides an instance of CompanyService.
    """
    return CompanyService(company_repo)
