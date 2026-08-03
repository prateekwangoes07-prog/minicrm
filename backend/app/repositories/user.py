from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User


class UserRepository:
    """
    Repository for handling database operations for the User model.
    """
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_email(self, email: str) -> User | None:
        """
        Retrieve a user by their email address.
        """
        stmt = select(User).where(User.email == email)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def create(self, user: User) -> User:
        """
        Add, flush and refresh a new user record in the database.
        Commit is managed at the service level.
        """
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return user
