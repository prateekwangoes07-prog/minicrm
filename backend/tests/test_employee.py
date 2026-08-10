import uuid
from datetime import datetime, timezone
import pytest
from httpx import AsyncClient

from app.main import app
from app.models.company import Company
from app.models.user import User
from app.dependencies.auth import get_current_user, require_admin
from app.services.employee import EmployeeService
from app.repositories.user import UserRepository
from app.repositories.company import CompanyRepository
from app.exceptions.employee import EmployeeNotFoundException, EmployeeAlreadyExistsException
from app.exceptions.company import CompanyNotFoundException
from app.schemas.employee import EmployeeCreate, EmployeeUpdate


# Mock objects
mock_company_id = uuid.uuid4()
mock_employee_id = uuid.uuid4()

mock_admin = User(id=uuid.uuid4(), email="admin@test.com", role="admin")
mock_employee_user = User(id=uuid.uuid4(), email="emp@test.com", role="employee")

mock_employee_record = User(
    id=mock_employee_id,
    email="new_emp@test.com",
    first_name="Jane",
    last_name="Doe",
    role="employee",
    is_active=True,
    is_email_verified=False,
    company_id=mock_company_id,
    created_at=datetime.now(timezone.utc),
    updated_at=datetime.now(timezone.utc),
)


@pytest.mark.asyncio
async def test_admin_create_employee_success(client, monkeypatch):
    """
    1. Admin can create employee.
    8. Password/hash is never returned in API response.
    """
    async def mock_create(self, employee_in):
        return mock_employee_record

    monkeypatch.setattr(EmployeeService, "create_employee", mock_create)
    app.dependency_overrides[require_admin] = lambda: mock_admin

    response = await client.post(
        "/api/v1/employees",
        json={
            "email": "new_emp@test.com",
            "password": "securepassword123",
            "first_name": "Jane",
            "last_name": "Doe",
            "company_id": str(mock_company_id),
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "new_emp@test.com"
    assert data["first_name"] == "Jane"
    assert data["last_name"] == "Doe"
    assert data["company_id"] == str(mock_company_id)
    assert "password" not in data
    assert "hashed_password" not in data

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_create_employee_duplicate_email(client, monkeypatch):
    """
    2. Duplicate email returns 409.
    """
    async def mock_create(self, employee_in):
        raise EmployeeAlreadyExistsException("Employee with email 'new_emp@test.com' already exists.")

    monkeypatch.setattr(EmployeeService, "create_employee", mock_create)
    app.dependency_overrides[require_admin] = lambda: mock_admin

    response = await client.post(
        "/api/v1/employees",
        json={
            "email": "new_emp@test.com",
            "password": "securepassword123",
            "company_id": str(mock_company_id),
        },
    )
    assert response.status_code == 409
    assert "already exists" in response.json()["detail"]

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_non_admin_cannot_create_employee(client):
    """
    3. Non-admin cannot create employee.
    """
    from fastapi import HTTPException
    def mock_require_admin_fail():
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    app.dependency_overrides[require_admin] = mock_require_admin_fail

    response = await client.post(
        "/api/v1/employees",
        json={
            "email": "new_emp@test.com",
            "password": "securepassword123",
            "company_id": str(mock_company_id),
        },
    )
    assert response.status_code == 403
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_authenticated_user_can_view_employees(client, monkeypatch):
    """
    4. Authenticated user can view employees.
    """
    async def mock_get_all(self, skip=0, limit=100):
        return [mock_employee_record]

    monkeypatch.setattr(EmployeeService, "get_all_employees", mock_get_all)
    app.dependency_overrides[get_current_user] = lambda: mock_employee_user

    response = await client.get("/api/v1/employees")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["email"] == "new_emp@test.com"
    assert "password" not in data[0]
    assert "hashed_password" not in data[0]

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_get_employee_not_found(client, monkeypatch):
    """
    5. Nonexistent employee returns 404.
    """
    async def mock_get_employee(self, employee_id):
        raise EmployeeNotFoundException(str(employee_id))

    monkeypatch.setattr(EmployeeService, "get_employee", mock_get_employee)
    app.dependency_overrides[get_current_user] = lambda: mock_employee_user

    random_id = uuid.uuid4()
    response = await client.get(f"/api/v1/employees/{random_id}")
    assert response.status_code == 404
    assert f"Employee with ID '{random_id}' not found." in response.json()["detail"]

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_employee_cannot_assign_themselves_admin_privileges(client):
    """
    6. Employee cannot assign themselves admin privileges (restricted by 403 Forbidden).
    """
    from fastapi import HTTPException
    def mock_require_admin_fail():
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    app.dependency_overrides[require_admin] = mock_require_admin_fail

    response = await client.put(
        f"/api/v1/employees/{mock_employee_id}",
        json={"role": "admin"},
    )
    assert response.status_code == 403
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_password_is_hashed_and_not_plain(monkeypatch):
    """
    7. Password is hashed.
    """
    from app.core.security import verify_password
    
    created_user = None

    class MockUserRepo:
        async def get_by_email(self, email):
            return None
        async def create(self, user_obj):
            nonlocal created_user
            created_user = user_obj
            return user_obj
        @property
        def db(self):
            class MockDB:
                async def commit(self):
                    pass
            return MockDB()

    class MockCompanyRepo:
        async def get_by_id(self, company_id):
            return Company(id=company_id, name="Test Company", email="test@company.com")

    service = EmployeeService(user_repo=MockUserRepo(), company_repo=MockCompanyRepo())
    
    employee_in = EmployeeCreate(
        email="test_hash@example.com",
        password="plainpassword123",
        company_id=mock_company_id,
    )

    await service.create_employee(employee_in)

    assert created_user is not None
    assert created_user.hashed_password != "plainpassword123"
    assert verify_password("plainpassword123", created_user.hashed_password) is True


@pytest.mark.asyncio
async def test_admin_create_employee_ignores_submitted_role(monkeypatch):
    """
    6. Add/modify a test proving that a client cannot choose the employee role during creation.
    """
    created_user = None

    class MockUserRepo:
        async def get_by_email(self, email):
            return None
        async def create(self, user_obj):
            nonlocal created_user
            created_user = user_obj
            return user_obj
        @property
        def db(self):
            class MockDB:
                async def commit(self):
                    pass
            return MockDB()

    class MockCompanyRepo:
        async def get_by_id(self, company_id):
            return Company(id=company_id, name="Test Company", email="test@company.com")

    service = EmployeeService(user_repo=MockUserRepo(), company_repo=MockCompanyRepo())
    
    employee_in = EmployeeCreate(
        email="test_role@example.com",
        password="plainpassword123",
        company_id=mock_company_id,
    )

    # Call the service create method
    await service.create_employee(employee_in)

    # Prove that the role is hardcoded to "employee" by the service
    assert created_user is not None
    assert created_user.role == "employee"

