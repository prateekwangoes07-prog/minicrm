from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.repositories.customer import CustomerRepository
from app.repositories.company import CompanyRepository
from app.services.customer import CustomerService
from app.dependencies.company import get_company_repository


def get_customer_repository(db: AsyncSession = Depends(get_db)) -> CustomerRepository:
    """
    Dependency that provides an instance of CustomerRepository.
    """
    return CustomerRepository(db)


def get_customer_service(
    customer_repo: CustomerRepository = Depends(get_customer_repository),
    company_repo: CompanyRepository = Depends(get_company_repository),
) -> CustomerService:
    """
    Dependency that provides an instance of CustomerService.
    """
    return CustomerService(customer_repo, company_repo)
