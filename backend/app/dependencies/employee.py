from fastapi import Depends
from app.repositories.user import UserRepository
from app.repositories.company import CompanyRepository
from app.services.employee import EmployeeService
from app.dependencies.user import get_user_repository
from app.dependencies.company import get_company_repository


def get_employee_service(
    user_repo: UserRepository = Depends(get_user_repository),
    company_repo: CompanyRepository = Depends(get_company_repository),
) -> EmployeeService:
    """
    Dependency that provides an instance of EmployeeService.
    """
    return EmployeeService(user_repo, company_repo)
