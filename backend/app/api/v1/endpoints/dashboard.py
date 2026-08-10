from fastapi import APIRouter, Depends, status

from app.dependencies.auth import get_current_user
from app.dependencies.dashboard import get_dashboard_service
from app.schemas.dashboard import DashboardSummaryResponse
from app.services.dashboard import DashboardService

router = APIRouter()


@router.get(
    "/summary",
    response_model=DashboardSummaryResponse,
    status_code=status.HTTP_200_OK,
    summary="Get dashboard statistics summary",
    description="Retrieves a summary of the CRM metrics including totals and statuses. Accessible to all authenticated users.",
)
async def get_dashboard_summary(
    dashboard_service: DashboardService = Depends(get_dashboard_service),
    _: None = Depends(get_current_user),
) -> DashboardSummaryResponse:
    """
    Get dashboard metrics.
    """
    return await dashboard_service.get_summary()
