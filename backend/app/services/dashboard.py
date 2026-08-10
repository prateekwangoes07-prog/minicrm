from app.repositories.dashboard import DashboardRepository
from app.schemas.dashboard import DashboardSummaryResponse, DashboardLeadStatus, EmployeeLeadCount


class DashboardService:
    """
    Service layer containing business logic for Dashboard statistics aggregations.
    """
    def __init__(self, dashboard_repo: DashboardRepository) -> None:
        self.dashboard_repo = dashboard_repo

    async def get_summary(self) -> DashboardSummaryResponse:
        """
        Gathers dashboard metrics, formats them, calculates conversion rates, and returns the response schema.
        """
        total_companies = await self.dashboard_repo.get_total_companies()
        total_employees = await self.dashboard_repo.get_total_employees()
        total_customers = await self.dashboard_repo.get_total_customers()
        total_leads = await self.dashboard_repo.get_total_leads()

        # Status counts mapping
        status_map = await self.dashboard_repo.get_leads_by_status()
        leads_by_status = DashboardLeadStatus(
            new=status_map.get("new", 0),
            contacted=status_map.get("contacted", 0),
            qualified=status_map.get("qualified", 0),
            proposal=status_map.get("proposal", 0),
            won=status_map.get("won", 0),
            lost=status_map.get("lost", 0),
        )

        # Lead conversion rate calculation
        if total_leads > 0:
            lead_conversion_rate = float(leads_by_status.won) / float(total_leads)
        else:
            lead_conversion_rate = 0.0

        # Assigned leads to employees
        assigned_data = await self.dashboard_repo.get_leads_assigned_to_employees()
        leads_assigned = [
            EmployeeLeadCount(
                employee_id=item["employee_id"],
                employee_email=item["employee_email"],
                lead_count=item["lead_count"],
            )
            for item in assigned_data
        ]

        return DashboardSummaryResponse(
            total_companies=total_companies,
            total_employees=total_employees,
            total_customers=total_customers,
            total_leads=total_leads,
            leads_by_status=leads_by_status,
            lead_conversion_rate=lead_conversion_rate,
            leads_assigned_to_employees=leads_assigned,
        )
