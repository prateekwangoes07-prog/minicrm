from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.repositories.lead import LeadRepository
from app.repositories.company import CompanyRepository
from app.repositories.customer import CustomerRepository
from app.repositories.user import UserRepository
from app.services.lead import LeadService
from app.dependencies.company import get_company_repository
from app.dependencies.customer import get_customer_repository
from app.dependencies.user import get_user_repository


def get_lead_repository(db: AsyncSession = Depends(get_db)) -> LeadRepository:
    """
    Dependency that provides an instance of LeadRepository.
    """
    return LeadRepository(db)


def get_lead_service(
    lead_repo: LeadRepository = Depends(get_lead_repository),
    company_repo: CompanyRepository = Depends(get_company_repository),
    customer_repo: CustomerRepository = Depends(get_customer_repository),
    user_repo: UserRepository = Depends(get_user_repository),
) -> LeadService:
    """
    Dependency that provides an instance of LeadService.
    """
    return LeadService(lead_repo, company_repo, customer_repo, user_repo)
