import uuid
from datetime import datetime, timezone
import pytest
from app.main import app
from app.models.user import User
from app.models.lead import Lead
from app.dependencies.auth import get_current_user
from app.services.lead import LeadService
from app.exceptions.lead import LeadNotFoundException, InvalidLeadRelationshipException


mock_admin = User(id=uuid.uuid4(), email="admin@test.com", role="admin")
mock_employee = User(id=uuid.uuid4(), email="emp@test.com", role="employee")

mock_company_id = uuid.uuid4()
mock_lead_id = uuid.uuid4()
mock_lead = Lead(
    id=mock_lead_id,
    company_id=mock_company_id,
    customer_id=None,
    assigned_to=None,
    name="Test Lead",
    email="lead@test.com",
    phone="1234567890",
    requirement="Need custom software development",
    status="new",
    source="Website",
    notes="Some notes",
    created_at=datetime.now(timezone.utc),
    updated_at=datetime.now(timezone.utc),
)


@pytest.fixture(autouse=True)
def clean_overrides():
    app.dependency_overrides.clear()
    yield
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_admin_can_create_lead(client, monkeypatch):
    """
    12. Admin can create lead.
    """
    async def mock_create(self, lead_in):
        return mock_lead

    monkeypatch.setattr(LeadService, "create_lead", mock_create)
    app.dependency_overrides[get_current_user] = lambda: mock_admin

    response = await client.post(
        "/api/v1/leads",
        json={
            "name": "Test Lead",
            "email": "lead@test.com",
            "company_id": str(mock_company_id),
            "status": "new",
        },
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Test Lead"


@pytest.mark.asyncio
async def test_employee_cannot_create_lead(client):
    """
    13. Employee cannot create lead.
    """
    app.dependency_overrides[get_current_user] = lambda: mock_employee

    response = await client.post(
        "/api/v1/leads",
        json={
            "name": "Test Lead",
            "email": "lead@test.com",
            "company_id": str(mock_company_id),
            "status": "new",
        },
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_authenticated_user_can_list_leads(client, monkeypatch):
    """
    14. Authenticated user can list leads.
    """
    async def mock_get_all(self, company_id=None, customer_id=None, assigned_to=None, status=None, skip=0, limit=100):
        return [mock_lead]

    monkeypatch.setattr(LeadService, "get_all_leads", mock_get_all)
    app.dependency_overrides[get_current_user] = lambda: mock_employee

    response = await client.get("/api/v1/leads")
    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_authenticated_user_can_retrieve_lead(client, monkeypatch):
    """
    15. Authenticated user can retrieve lead.
    """
    async def mock_get(self, lead_id):
        return mock_lead

    monkeypatch.setattr(LeadService, "get_lead", mock_get)
    app.dependency_overrides[get_current_user] = lambda: mock_employee

    response = await client.get(f"/api/v1/leads/{mock_lead_id}")
    assert response.status_code == 200
    assert response.json()["id"] == str(mock_lead_id)


@pytest.mark.asyncio
async def test_admin_can_update_lead(client, monkeypatch):
    """
    16. Admin can update lead.
    """
    async def mock_update(self, lead_id, lead_in):
        return mock_lead

    monkeypatch.setattr(LeadService, "update_lead", mock_update)
    app.dependency_overrides[get_current_user] = lambda: mock_admin

    response = await client.put(
        f"/api/v1/leads/{mock_lead_id}",
        json={"name": "Updated Lead Name"},
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_employee_cannot_update_lead(client):
    """
    17. Employee cannot update lead.
    """
    app.dependency_overrides[get_current_user] = lambda: mock_employee

    response = await client.put(
        f"/api/v1/leads/{mock_lead_id}",
        json={"name": "Updated Lead Name"},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_admin_can_delete_lead(client, monkeypatch):
    """
    18. Admin can delete lead.
    """
    async def mock_delete(self, lead_id):
        pass

    monkeypatch.setattr(LeadService, "delete_lead", mock_delete)
    app.dependency_overrides[get_current_user] = lambda: mock_admin

    response = await client.delete(f"/api/v1/leads/{mock_lead_id}")
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_employee_cannot_delete_lead(client):
    """
    19. Employee cannot delete lead.
    """
    app.dependency_overrides[get_current_user] = lambda: mock_employee

    response = await client.delete(f"/api/v1/leads/{mock_lead_id}")
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_invalid_company_returns_404(client, monkeypatch):
    """
    20. Invalid company returns 404.
    """
    async def mock_create(self, lead_in):
        raise InvalidLeadRelationshipException(f"Company with ID '{lead_in.company_id}' not found.")

    monkeypatch.setattr(LeadService, "create_lead", mock_create)
    app.dependency_overrides[get_current_user] = lambda: mock_admin

    response = await client.post(
        "/api/v1/leads",
        json={
            "name": "Test Lead",
            "email": "lead@test.com",
            "company_id": str(uuid.uuid4()),
            "status": "new",
        },
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_invalid_customer_returns_404(client, monkeypatch):
    """
    21. Invalid customer returns 404.
    """
    async def mock_create(self, lead_in):
        raise InvalidLeadRelationshipException(f"Customer with ID '{lead_in.customer_id}' not found.")

    monkeypatch.setattr(LeadService, "create_lead", mock_create)
    app.dependency_overrides[get_current_user] = lambda: mock_admin

    response = await client.post(
        "/api/v1/leads",
        json={
            "name": "Test Lead",
            "email": "lead@test.com",
            "company_id": str(mock_company_id),
            "customer_id": str(uuid.uuid4()),
            "status": "new",
        },
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_invalid_assigned_employee_returns_404(client, monkeypatch):
    """
    22. Invalid assigned employee returns 404.
    """
    async def mock_create(self, lead_in):
        raise InvalidLeadRelationshipException(f"User with ID '{lead_in.assigned_to}' not found.")

    monkeypatch.setattr(LeadService, "create_lead", mock_create)
    app.dependency_overrides[get_current_user] = lambda: mock_admin

    response = await client.post(
        "/api/v1/leads",
        json={
            "name": "Test Lead",
            "email": "lead@test.com",
            "company_id": str(mock_company_id),
            "assigned_to": str(uuid.uuid4()),
            "status": "new",
        },
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_invalid_lead_status_is_rejected(client):
    """
    23. Invalid lead status is rejected.
    """
    app.dependency_overrides[get_current_user] = lambda: mock_admin

    response = await client.post(
        "/api/v1/leads",
        json={
            "name": "Test Lead",
            "email": "lead@test.com",
            "company_id": str(mock_company_id),
            "status": "invalid_status",
        },
    )
    assert response.status_code == 422
