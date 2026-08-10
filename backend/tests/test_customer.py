import uuid
from datetime import datetime, timezone
import pytest
from app.main import app
from app.models.user import User
from app.models.company import Company
from app.models.customer import Customer
from app.dependencies.auth import get_current_user
from app.services.customer import CustomerService
from app.exceptions.customer import CustomerNotFoundException, CustomerAlreadyExistsException
from app.exceptions.company import CompanyNotFoundException


mock_admin = User(id=uuid.uuid4(), email="admin@test.com", role="admin")
mock_employee = User(id=uuid.uuid4(), email="emp@test.com", role="employee")

mock_company_id = uuid.uuid4()
mock_customer_id = uuid.uuid4()
mock_customer = Customer(
    id=mock_customer_id,
    company_id=mock_company_id,
    first_name="John",
    last_name="Doe",
    email="john@doe.com",
    phone="1234567890",
    address="123 Customer Rd",
    notes="Some notes",
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
async def test_admin_can_create_customer(client, monkeypatch):
    """
    1. Admin can create customer.
    """
    async def mock_create(self, customer_in):
        return mock_customer

    monkeypatch.setattr(CustomerService, "create_customer", mock_create)
    app.dependency_overrides[get_current_user] = lambda: mock_admin

    response = await client.post(
        "/api/v1/customers",
        json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@doe.com",
            "company_id": str(mock_company_id),
        },
    )
    assert response.status_code == 201
    assert response.json()["email"] == "john@doe.com"


@pytest.mark.asyncio
async def test_employee_cannot_create_customer(client):
    """
    2. Employee cannot create customer.
    """
    app.dependency_overrides[get_current_user] = lambda: mock_employee

    response = await client.post(
        "/api/v1/customers",
        json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@doe.com",
            "company_id": str(mock_company_id),
        },
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_authenticated_user_can_list_customers(client, monkeypatch):
    """
    3. Authenticated user can list customers.
    """
    async def mock_get_all(self, skip=0, limit=100):
        return [mock_customer]

    monkeypatch.setattr(CustomerService, "get_all_customers", mock_get_all)
    app.dependency_overrides[get_current_user] = lambda: mock_employee

    response = await client.get("/api/v1/customers")
    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_authenticated_user_can_retrieve_customer(client, monkeypatch):
    """
    4. Authenticated user can retrieve customer.
    """
    async def mock_get(self, customer_id):
        return mock_customer

    monkeypatch.setattr(CustomerService, "get_customer", mock_get)
    app.dependency_overrides[get_current_user] = lambda: mock_employee

    response = await client.get(f"/api/v1/customers/{mock_customer_id}")
    assert response.status_code == 200
    assert response.json()["id"] == str(mock_customer_id)


@pytest.mark.asyncio
async def test_admin_can_update_customer(client, monkeypatch):
    """
    5. Admin can update customer.
    """
    async def mock_update(self, customer_id, customer_in):
        return mock_customer

    monkeypatch.setattr(CustomerService, "update_customer", mock_update)
    app.dependency_overrides[get_current_user] = lambda: mock_admin

    response = await client.put(
        f"/api/v1/customers/{mock_customer_id}",
        json={"first_name": "UpdatedName"},
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_employee_cannot_update_customer(client):
    """
    6. Employee cannot update customer.
    """
    app.dependency_overrides[get_current_user] = lambda: mock_employee

    response = await client.put(
        f"/api/v1/customers/{mock_customer_id}",
        json={"first_name": "UpdatedName"},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_admin_can_delete_customer(client, monkeypatch):
    """
    7. Admin can delete customer.
    """
    async def mock_delete(self, customer_id):
        pass

    monkeypatch.setattr(CustomerService, "delete_customer", mock_delete)
    app.dependency_overrides[get_current_user] = lambda: mock_admin

    response = await client.delete(f"/api/v1/customers/{mock_customer_id}")
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_employee_cannot_delete_customer(client):
    """
    8. Employee cannot delete customer.
    """
    app.dependency_overrides[get_current_user] = lambda: mock_employee

    response = await client.delete(f"/api/v1/customers/{mock_customer_id}")
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_duplicate_customer_email_returns_409(client, monkeypatch):
    """
    9. Duplicate customer email returns 409.
    """
    async def mock_create(self, customer_in):
        raise CustomerAlreadyExistsException("Customer with email already exists.")

    monkeypatch.setattr(CustomerService, "create_customer", mock_create)
    app.dependency_overrides[get_current_user] = lambda: mock_admin

    response = await client.post(
        "/api/v1/customers",
        json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "duplicate@doe.com",
            "company_id": str(mock_company_id),
        },
    )
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_invalid_company_returns_404(client, monkeypatch):
    """
    10. Invalid company returns 404.
    """
    async def mock_create(self, customer_in):
        raise CompanyNotFoundException(str(customer_in.company_id))

    monkeypatch.setattr(CustomerService, "create_customer", mock_create)
    app.dependency_overrides[get_current_user] = lambda: mock_admin

    response = await client.post(
        "/api/v1/customers",
        json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@doe.com",
            "company_id": str(uuid.uuid4()),
        },
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_missing_authentication_returns_401(client):
    """
    11. Missing authentication returns 401.
    """
    response = await client.get("/api/v1/customers")
    assert response.status_code == 401
