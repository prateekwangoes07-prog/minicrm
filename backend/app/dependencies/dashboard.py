from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.repositories.dashboard import DashboardRepository
from app.services.dashboard import DashboardService


def get_dashboard_repository(db: AsyncSession = Depends(get_db)) -> DashboardRepository:
    """
    Dependency that provides an instance of DashboardRepository.
    """
    return DashboardRepository(db)


def get_dashboard_service(
    dashboard_repo: DashboardRepository = Depends(get_dashboard_repository),
) -> DashboardService:
    """
    Dependency that provides an instance of DashboardService.
    """
    return DashboardService(dashboard_repo)
