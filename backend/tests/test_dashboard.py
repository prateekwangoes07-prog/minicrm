import uuid
import pytest
from app.main import app
from app.models.user import User
from app.dependencies.auth import get_current_user
from app.services.dashboard import DashboardService
from app.schemas.dashboard import DashboardSummaryResponse, DashboardLeadStatus, EmployeeLeadCount


mock_employee = User(id=uuid.uuid4(), email="emp@test.com", role="employee")

mock_dashboard_summary = DashboardSummaryResponse(
    total_companies=10,
    total_employees=5,
    total_customers=20,
    total_leads=10,
    leads_by_status=DashboardLeadStatus(
        new=2,
        contacted=3,
        qualified=1,
        proposal=1,
        won=2,
        lost=1,
    ),
    lead_conversion_rate=0.2,
    leads_assigned_to_employees=[
        EmployeeLeadCount(
            employee_id=uuid.uuid4(),
            employee_email="emp1@test.com",
            lead_count=4,
        )
    ]
)


@pytest.fixture(autouse=True)
def clean_overrides():
    app.dependency_overrides.clear()
    yield
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_authenticated_user_can_fetch_summary(client, monkeypatch):
    """
    Test that an authenticated user can access the dashboard summary endpoint.
    """
    async def mock_get_summary(self):
        return mock_dashboard_summary

    monkeypatch.setattr(DashboardService, "get_summary", mock_get_summary)
    app.dependency_overrides[get_current_user] = lambda: mock_employee

    response = await client.get("/api/v1/dashboard/summary")
    assert response.status_code == 200
    data = response.json()
    assert data["total_companies"] == 10
    assert data["total_employees"] == 5
    assert data["total_customers"] == 20
    assert data["total_leads"] == 10
    assert data["leads_by_status"]["won"] == 2
    assert data["lead_conversion_rate"] == 0.2
    assert len(data["leads_assigned_to_employees"]) == 1


@pytest.mark.asyncio
async def test_dashboard_unauthenticated_returns_401(client):
    """
    Test that an unauthenticated request returns 401.
    """
    response = await client.get("/api/v1/dashboard/summary")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_conversion_rate_calculation():
    """
    Test conversion rate calculation in DashboardService.
    """
    from app.services.dashboard import DashboardService

    # 1. Total leads > 0
    class MockRepo:
        async def get_total_companies(self): return 1
        async def get_total_employees(self): return 1
        async def get_total_customers(self): return 1
        async def get_total_leads(self): return 10
        async def get_leads_by_status(self): return {"won": 2}
        async def get_leads_assigned_to_employees(self): return []

    service = DashboardService(MockRepo())
    summary = await service.get_summary()
    assert summary.lead_conversion_rate == 0.2

    # 2. Total leads = 0
    class MockRepoZero:
        async def get_total_companies(self): return 1
        async def get_total_employees(self): return 1
        async def get_total_customers(self): return 1
        async def get_total_leads(self): return 0
        async def get_leads_by_status(self): return {}
        async def get_leads_assigned_to_employees(self): return []

    service_zero = DashboardService(MockRepoZero())
    summary_zero = await service_zero.get_summary()
    assert summary_zero.lead_conversion_rate == 0.0
