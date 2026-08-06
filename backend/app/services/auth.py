from app.core.security import verify_password
from app.core.jwt import create_access_token
from app.exceptions.auth import AuthenticationFailedException
from app.repositories.auth import AuthRepository
from app.schemas.token import LoginRequest, Token

class AuthService:
    """
    Service layer containing business logic for authentication.
    """
    def __init__(self, auth_repo: AuthRepository) -> None:
        self.auth_repo = auth_repo

    async def authenticate_user(self, login_data: LoginRequest) -> Token:
        """
        Authenticate a user by email and password, returning a JWT token on success.
        """
        print("===== LOGIN DEBUG =====")
        print(f"Email received: {login_data.email}")
        
        user = await self.auth_repo.get_user_by_email(login_data.email)
        
        print(f"User found: {user is not None}")
        
        if user:
            print(f"DB Email: {user.email}")
            print(f"Hash: {user.hashed_password}")
            
        if not user:
            raise AuthenticationFailedException()

        result = verify_password(login_data.password, user.hashed_password)
        print(f"Password verification result: {result}")
        
        if not result:
            raise AuthenticationFailedException()

        print("JWT generation reached.")
        
        # Generate access token using the user's ID
        access_token = create_access_token(subject=user.id)
        
        return Token(
            access_token=access_token,
            token_type="bearer"
        )
