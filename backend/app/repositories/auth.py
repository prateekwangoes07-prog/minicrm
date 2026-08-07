from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User

class AuthRepository:
    """
    Repository for authentication database operations.
    """
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_user_by_id(self, user_id: str) -> User | None:
        """
        Retrieve a user by their primary-key ID.

        Args:
            user_id: Stringified UUID (as stored in the JWT ``sub`` claim).

        Returns:
            The matching ``User`` or ``None`` if no row exists.
        """
        from uuid import UUID

        try:
            uid = UUID(user_id)
        except ValueError:
            return None

        stmt = select(User).where(User.id == uid)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def get_user_by_email(self, email: str) -> User | None:
        """
        Retrieve a user by their email address for authentication purposes.
        """
        stmt = select(User).where(User.email == email)
        result = await self.db.execute(stmt)
        return result.scalars().first()
