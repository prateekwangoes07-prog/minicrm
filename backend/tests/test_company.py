import uuid
from datetime import datetime, timezone
import pytest
from httpx import AsyncClient

from app.main import app
from app.models.company import Company
from app.models.user import User
from app.dependencies.auth import get_current_user, require_admin
from app.dependencies.company import get_company_service
from app.services.company import CompanyService
from app.exceptions.company import CompanyAlreadyExistsException, CompanyNotFoundException

# Create mock data
mock_company_id = uuid.uuid4()
mock_company = Company(
    id=mock_company_id,
    name="Test Company LLC",
    email="contact@testcompany.com",
    phone="1234567890",
    address="123 Main St",
    website_url="https://testcompany.com",
    industry="Tech",
    is_active=True,
    created_at=datetime.now(timezone.utc),
    updated_at=datetime.now(timezone.utc),
)

mock_admin = User(id=uuid.uuid4(), email="admin@test.com", role="admin")
mock_employee = User(id=uuid.uuid4(), email="emp@test.com", role="employee")


@pytest.mark.asyncio
async def test_create_company_admin_success(client, monkeypatch):
    """
    Test creating a company successfully as an administrator.
    """
    async def mock_create(self, company_in):
        return mock_company

    monkeypatch.setattr(CompanyService, "create_company", mock_create)

    # Override authorization dependencies
    app.dependency_overrides[require_admin] = lambda: mock_admin

    response = await client.post(
        "/api/v1/companies",
        json={
            "name": "Test Company LLC",
            "email": "contact@testcompany.com",
            "phone": "1234567890",
            "address": "123 Main St",
            "website_url": "https://testcompany.com",
            "industry": "Tech",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Company LLC"
    assert data["email"] == "contact@testcompany.com"

    # Clean up overrides
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_create_company_duplicate(client, monkeypatch):
    """
    Test creating a company with a duplicate name or email.
    """
    async def mock_create(self, company_in):
        raise CompanyAlreadyExistsException("Company with name 'Test Company LLC' already exists.")

    monkeypatch.setattr(CompanyService, "create_company", mock_create)

    app.dependency_overrides[require_admin] = lambda: mock_admin

    response = await client.post(
        "/api/v1/companies",
        json={
            "name": "Test Company LLC",
            "email": "contact@testcompany.com",
        },
    )
    assert response.status_code == 409
    assert "already exists" in response.json()["detail"]

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_list_companies_authenticated(client, monkeypatch):
    """
    Test listing companies as an authenticated user.
    """
    async def mock_get_all(self, skip=0, limit=100):
        return [mock_company]

    monkeypatch.setattr(CompanyService, "get_all_companies", mock_get_all)

    app.dependency_overrides[get_current_user] = lambda: mock_employee

    response = await client.get("/api/v1/companies")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Test Company LLC"

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_get_company_not_found(client, monkeypatch):
    """
    Test retrieving a non-existent company.
    """
    async def mock_get_company(self, company_id):
        raise CompanyNotFoundException(str(company_id))

    monkeypatch.setattr(CompanyService, "get_company", mock_get_company)

    app.dependency_overrides[get_current_user] = lambda: mock_employee

    random_id = uuid.uuid4()
    response = await client.get(f"/api/v1/companies/{random_id}")
    assert response.status_code == 404
    assert f"Company with ID '{random_id}' not found." in response.json()["detail"]

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_update_company_admin_success(client, monkeypatch):
    """
    Test updating a company successfully as an administrator.
    """
    async def mock_update(self, company_id, company_in):
        return mock_company

    monkeypatch.setattr(CompanyService, "update_company", mock_update)

    app.dependency_overrides[require_admin] = lambda: mock_admin

    response = await client.put(
        f"/api/v1/companies/{mock_company_id}",
        json={"name": "Updated Company Name"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(mock_company_id)

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_delete_company_admin_success(client, monkeypatch):
    """
    Test deleting a company successfully as an administrator.
    """
    async def mock_delete(self, company_id):
        pass

    monkeypatch.setattr(CompanyService, "delete_company", mock_delete)

    app.dependency_overrides[require_admin] = lambda: mock_admin

    response = await client.delete(f"/api/v1/companies/{mock_company_id}")
    assert response.status_code == 204

    app.dependency_overrides.clear()
