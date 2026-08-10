from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.company import Company
from app.models.user import User
from app.models.customer import Customer
from app.models.lead import Lead


class DashboardRepository:
    """
    Repository for performing dashboard aggregation queries on the database.
    """
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_total_companies(self) -> int:
        stmt = select(func.count(Company.id))
        result = await self.db.execute(stmt)
        return result.scalar() or 0

    async def get_total_employees(self) -> int:
        stmt = select(func.count(User.id)).where(User.role == "employee")
        result = await self.db.execute(stmt)
        return result.scalar() or 0

    async def get_total_customers(self) -> int:
        stmt = select(func.count(Customer.id))
        result = await self.db.execute(stmt)
        return result.scalar() or 0

    async def get_total_leads(self) -> int:
        stmt = select(func.count(Lead.id))
        result = await self.db.execute(stmt)
        return result.scalar() or 0

    async def get_leads_by_status(self) -> dict[str, int]:
        stmt = select(Lead.status, func.count(Lead.id)).group_by(Lead.status)
        result = await self.db.execute(stmt)
        rows = result.all()
        return {status: count for status, count in rows}

    async def get_leads_assigned_to_employees(self) -> list[dict]:
        stmt = (
            select(User.id, User.email, func.count(Lead.id).label("lead_count"))
            .outerjoin(Lead, User.id == Lead.assigned_to)
            .where(User.role == "employee")
            .group_by(User.id, User.email)
        )
        result = await self.db.execute(stmt)
        rows = result.all()
        return [
            {
                "employee_id": row.id,
                "employee_email": row.email,
                "lead_count": row.lead_count,
            }
            for row in rows
        ]
