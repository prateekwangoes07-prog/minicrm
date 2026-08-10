from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.lead import Lead


class LeadRepository:
    """
    Repository for handling database operations for the Lead model.
    """
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_id(self, lead_id: UUID) -> Lead | None:
        """
        Retrieve a lead by its primary key UUID.
        """
        stmt = select(Lead).where(Lead.id == lead_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def get_all(
        self,
        company_id: UUID | None = None,
        customer_id: UUID | None = None,
        assigned_to: UUID | None = None,
        status: str | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Lead]:
        """
        Retrieve leads with optional filtering and pagination.
        """
        stmt = select(Lead)
        if company_id is not None:
            stmt = stmt.where(Lead.company_id == company_id)
        if customer_id is not None:
            stmt = stmt.where(Lead.customer_id == customer_id)
        if assigned_to is not None:
            stmt = stmt.where(Lead.assigned_to == assigned_to)
        if status is not None:
            stmt = stmt.where(Lead.status == status)

        stmt = stmt.offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create(self, lead: Lead) -> Lead:
        """
        Add a new lead record, flush and refresh it.
        """
        self.db.add(lead)
        await self.db.flush()
        await self.db.refresh(lead)
        return lead

    async def update(self, lead: Lead) -> Lead:
        """
        Update a lead record, flush and refresh it.
        """
        self.db.add(lead)
        await self.db.flush()
        await self.db.refresh(lead)
        return lead

    async def delete(self, lead: Lead) -> None:
        """
        Delete a lead record.
        """
        await self.db.delete(lead)
        await self.db.flush()
