from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.customer import Customer


class CustomerRepository:
    """
    Repository for handling database operations for the Customer model.
    """
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_id(self, customer_id: UUID) -> Customer | None:
        """
        Retrieve a customer by their primary key UUID.
        """
        stmt = select(Customer).where(Customer.id == customer_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def get_by_email(self, email: str) -> Customer | None:
        """
        Retrieve a customer by their email address.
        """
        stmt = select(Customer).where(Customer.email == email)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def get_by_company_id(self, company_id: UUID, skip: int = 0, limit: int = 100) -> list[Customer]:
        """
        Retrieve all customers belonging to a specific company.
        """
        stmt = select(Customer).where(Customer.company_id == company_id).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[Customer]:
        """
        Retrieve all customers with optional pagination.
        """
        stmt = select(Customer).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create(self, customer: Customer) -> Customer:
        """
        Add a new customer record, flush and refresh it.
        """
        self.db.add(customer)
        await self.db.flush()
        await self.db.refresh(customer)
        return customer

    async def update(self, customer: Customer) -> Customer:
        """
        Update a customer record, flush and refresh it.
        """
        self.db.add(customer)
        await self.db.flush()
        await self.db.refresh(customer)
        return customer

    async def delete(self, customer: Customer) -> None:
        """
        Delete a customer record.
        """
        await self.db.delete(customer)
        await self.db.flush()
