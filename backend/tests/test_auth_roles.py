import uuid
from datetime import datetime, timezone
import pytest
from app.main import app
from app.models.user import User
from app.models.company import Company
from app.dependencies.auth import get_current_user
from app.services.company import CompanyService
from app.services.employee import EmployeeService


mock_admin = User(
    id=uuid.uuid4(),
    email="admin@test.com",
    role="admin",
    is_active=True,
    is_email_verified=True,
    created_at=datetime.now(timezone.utc),
    updated_at=datetime.now(timezone.utc),
)
mock_employee = User(
    id=uuid.uuid4(),
    email="emp@test.com",
    role="employee",
    is_active=True,
    is_email_verified=True,
    created_at=datetime.now(timezone.utc),
    updated_at=datetime.now(timezone.utc),
)
mock_company = Company(
    id=uuid.uuid4(),
    name="Test Company",
    email="test@company.com",
    is_active=True,
    created_at=datetime.now(timezone.utc),
    updated_at=datetime.now(timezone.utc),
)


@pytest.fixture(autouse=True)
def clean_overrides():
    app.dependency_overrides.clear()
    yield
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_admin_can_access_admin_endpoints(client, monkeypatch):
    """
    Test admin access to at least one admin-only Company endpoint and one admin-only Employee endpoint.
    """
    # Mock Company service
    async def mock_create_company(self, company_in):
        return mock_company
    monkeypatch.setattr(CompanyService, "create_company", mock_create_company)

    # Mock Employee service
    async def mock_create_employee(self, employee_in):
        return mock_employee
    monkeypatch.setattr(EmployeeService, "create_employee", mock_create_employee)

    app.dependency_overrides[get_current_user] = lambda: mock_admin

    # Admin access to POST /api/v1/companies
    response_company = await client.post(
        "/api/v1/companies",
        json={
            "name": "Test Company",
            "email": "test@company.com",
        },
    )
    assert response_company.status_code == 201

    # Admin access to POST /api/v1/employees
    response_employee = await client.post(
        "/api/v1/employees",
        json={
            "email": "emp_new@test.com",
            "password": "password123",
            "company_id": str(uuid.uuid4()),
        },
    )
    assert response_employee.status_code == 201


@pytest.mark.asyncio
async def test_employee_cannot_create_company(client):
    """
    Verify: employee -> POST /api/v1/companies -> 403, detail == "Not enough permissions"
    """
    app.dependency_overrides[get_current_user] = lambda: mock_employee

    response = await client.post(
        "/api/v1/companies",
        json={
            "name": "Unauthorized Company",
            "email": "unauth@company.com",
        },
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Not enough permissions"


@pytest.mark.asyncio
async def test_employee_cannot_modify_companies(client):
    """
    Verify employee receives 403 on other company modifications.
    """
    app.dependency_overrides[get_current_user] = lambda: mock_employee

    company_id = uuid.uuid4()

    response_put = await client.put(f"/api/v1/companies/{company_id}", json={"name": "New Name"})
    assert response_put.status_code == 403
    assert response_put.json()["detail"] == "Not enough permissions"

    response_delete = await client.delete(f"/api/v1/companies/{company_id}")
    assert response_delete.status_code == 403
    assert response_delete.json()["detail"] == "Not enough permissions"


@pytest.mark.asyncio
async def test_employee_cannot_modify_employees(client):
    """
    Verify employee access to:
    - POST /api/v1/employees → 403
    - PUT /api/v1/employees/{id} → 403
    - DELETE /api/v1/employees/{id} → 403
    """
    app.dependency_overrides[get_current_user] = lambda: mock_employee

    employee_id = uuid.uuid4()

    # Create employee
    response_post = await client.post(
        "/api/v1/employees",
        json={
            "email": "emp_new@test.com",
            "password": "password123",
            "company_id": str(uuid.uuid4()),
        },
    )
    assert response_post.status_code == 403
    assert response_post.json()["detail"] == "Not enough permissions"

    # Update employee
    response_put = await client.put(f"/api/v1/employees/{employee_id}", json={"first_name": "Jane"})
    assert response_put.status_code == 403
    assert response_put.json()["detail"] == "Not enough permissions"

    # Delete employee
    response_delete = await client.delete(f"/api/v1/employees/{employee_id}")
    assert response_delete.status_code == 403
    assert response_delete.json()["detail"] == "Not enough permissions"


@pytest.mark.asyncio
async def test_missing_token_receives_401(client):
    """
    Keep the existing tests for: missing token → 401
    """
    response = await client.get("/api/v1/companies")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_invalid_expired_token_receives_401(client):
    """
    Keep the existing tests for: invalid/expired token → 401
    """
    headers = {"Authorization": "Bearer invalidtoken123"}
    response = await client.get("/api/v1/companies", headers=headers)
    assert response.status_code == 401
    assert "Could not validate credentials" in response.json()["detail"]


@pytest.mark.asyncio
async def test_normal_authenticated_users_can_access_permitted_get_endpoints(client, monkeypatch):
    """
    Keep the existing tests for: authenticated GET access
    """
    async def mock_get_all(self, skip=0, limit=100):
        return []

    monkeypatch.setattr(CompanyService, "get_all_companies", mock_get_all)
    app.dependency_overrides[get_current_user] = lambda: mock_employee

    response = await client.get("/api/v1/companies")
    assert response.status_code == 200
