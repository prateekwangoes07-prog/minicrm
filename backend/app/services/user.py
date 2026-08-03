from app.core.security import get_password_hash
from app.exceptions.user import EmailAlreadyExistsException
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate


class UserService:
    """
    Service layer containing business logic for users.
    """
    def __init__(self, user_repo: UserRepository) -> None:
        self.user_repo = user_repo

    async def register_user(self, user_in: UserCreate) -> User:
        """
        Register a new user after validating email uniqueness and hashing the password.
        Manages the transaction commit after successful creation.
        """
        existing_user = await self.user_repo.get_by_email(user_in.email)
        if existing_user:
            raise EmailAlreadyExistsException(user_in.email)

        hashed_password = get_password_hash(user_in.password)
        
        db_user = User(
            email=user_in.email,
            hashed_password=hashed_password,
            first_name=user_in.first_name,
            last_name=user_in.last_name,
            role="employee",
            company_id=user_in.company_id,
        )
        created_user = await self.user_repo.create(db_user)
        await self.user_repo.db.commit()
        return created_user
