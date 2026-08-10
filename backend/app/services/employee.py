from uuid import UUID
from app.core.security import get_password_hash
from app.exceptions.employee import EmployeeNotFoundException, EmployeeAlreadyExistsException
from app.exceptions.company import CompanyNotFoundException
from app.models.user import User
from app.repositories.user import UserRepository
from app.repositories.company import CompanyRepository
from app.schemas.employee import EmployeeCreate, EmployeeUpdate


class EmployeeService:
    """
    Service layer containing business logic for Employee management.
    """
    def __init__(self, user_repo: UserRepository, company_repo: CompanyRepository) -> None:
        self.user_repo = user_repo
        self.company_repo = company_repo

    async def get_employee(self, employee_id: UUID) -> User:
        """
        Retrieve an employee by their ID.
        """
        employee = await self.user_repo.get_by_id(employee_id)
        if not employee:
            raise EmployeeNotFoundException(str(employee_id))
        return employee

    async def get_all_employees(self, skip: int = 0, limit: int = 100) -> list[User]:
        """
        Retrieve all employees with pagination.
        """
        return await self.user_repo.get_all(skip=skip, limit=limit)

    async def create_employee(self, employee_in: EmployeeCreate) -> User:
        """
        Create a new employee, checking email uniqueness and validating company existence.
        """
        # Validate company existence
        company = await self.company_repo.get_by_id(employee_in.company_id)
        if not company:
            raise CompanyNotFoundException(str(employee_in.company_id))

        # Check email uniqueness
        existing_user = await self.user_repo.get_by_email(employee_in.email)
        if existing_user:
            raise EmployeeAlreadyExistsException(f"Employee with email '{employee_in.email}' already exists.")

        # Hash password
        hashed_password = get_password_hash(employee_in.password)

        db_employee = User(
            email=employee_in.email,
            hashed_password=hashed_password,
            first_name=employee_in.first_name,
            last_name=employee_in.last_name,
            role="employee",
            company_id=employee_in.company_id,
        )

        created_employee = await self.user_repo.create(db_employee)
        await self.user_repo.db.commit()
        return created_employee

    async def update_employee(self, employee_id: UUID, employee_in: EmployeeUpdate) -> User:
        """
        Update an existing employee, checking uniqueness constraints and validating company existence.
        """
        employee = await self.user_repo.get_by_id(employee_id)
        if not employee:
            raise EmployeeNotFoundException(str(employee_id))

        # Validate company existence if it is being changed
        if employee_in.company_id is not None and employee_in.company_id != employee.company_id:
            company = await self.company_repo.get_by_id(employee_in.company_id)
            if not company:
                raise CompanyNotFoundException(str(employee_in.company_id))
            employee.company_id = employee_in.company_id

        # Validate email uniqueness if it is being changed
        if employee_in.email is not None and employee_in.email != employee.email:
            existing_user = await self.user_repo.get_by_email(employee_in.email)
            if existing_user:
                raise EmployeeAlreadyExistsException(f"Employee with email '{employee_in.email}' already exists.")
            employee.email = employee_in.email

        # Handle optional password change
        if employee_in.password is not None:
            employee.hashed_password = get_password_hash(employee_in.password)

        # Update other fields
        if employee_in.first_name is not None:
            employee.first_name = employee_in.first_name
        if employee_in.last_name is not None:
            employee.last_name = employee_in.last_name
        if employee_in.is_active is not None:
            employee.is_active = employee_in.is_active

        updated_employee = await self.user_repo.update(employee)
        await self.user_repo.db.commit()
        return updated_employee

    async def delete_employee(self, employee_id: UUID) -> None:
        """
        Delete an existing employee.
        """
        employee = await self.user_repo.get_by_id(employee_id)
        if not employee:
            raise EmployeeNotFoundException(str(employee_id))

        await self.user_repo.delete(employee)
        await self.user_repo.db.commit()
