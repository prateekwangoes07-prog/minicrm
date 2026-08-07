from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.company import Company


class CompanyRepository:
    """
    Repository for handling database operations for the Company model.
    """
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_id(self, company_id: UUID) -> Company | None:
        """
        Retrieve a company by its primary key ID.
        """
        stmt = select(Company).where(Company.id == company_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def get_by_name(self, name: str) -> Company | None:
        """
        Retrieve a company by its name.
        """
        stmt = select(Company).where(Company.name == name)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def get_by_email(self, email: str) -> Company | None:
        """
        Retrieve a company by its email address.
        """
        stmt = select(Company).where(Company.email == email)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[Company]:
        """
        Retrieve a list of companies with optional offset and limit pagination.
        """
        stmt = select(Company).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create(self, company: Company) -> Company:
        """
        Add a new company record, flush and refresh it.
        """
        self.db.add(company)
        await self.db.flush()
        await self.db.refresh(company)
        return company

    async def update(self, company: Company) -> Company:
        """
        Add/merge the updated company record, flush and refresh it.
        """
        self.db.add(company)
        await self.db.flush()
        await self.db.refresh(company)
        return company

    async def delete(self, company: Company) -> None:
        """
        Delete the company record from the database.
        """
        await self.db.delete(company)
        await self.db.flush()
