from uuid import UUID
from pydantic import BaseModel


class DashboardLeadStatus(BaseModel):
    new: int
    contacted: int
    qualified: int
    proposal: int
    won: int
    lost: int


class EmployeeLeadCount(BaseModel):
    employee_id: UUID | None
    employee_email: str | None
    lead_count: int


class DashboardSummaryResponse(BaseModel):
    total_companies: int
    total_employees: int
    total_customers: int
    total_leads: int
    leads_by_status: DashboardLeadStatus
    lead_conversion_rate: float
    leads_assigned_to_employees: list[EmployeeLeadCount]
