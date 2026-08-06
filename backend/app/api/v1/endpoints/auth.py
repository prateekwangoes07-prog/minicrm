from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies.user import get_user_service
from app.dependencies.auth import get_auth_service
from app.exceptions.user import EmailAlreadyExistsException
from app.exceptions.auth import AuthenticationFailedException
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.schemas.token import LoginRequest, Token
from app.services.user import UserService
from app.services.auth import AuthService

router = APIRouter()


@router.post(
    "/signup",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Creates a new user profile with email uniqueness checks and secure password hashing.",
)
async def signup(
    user_in: UserCreate,
    user_service: UserService = Depends(get_user_service),
) -> User:
    """
    User registration endpoint.
    """
    try:
        user = await user_service.register_user(user_in)
        return user
    except EmailAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        )


@router.post(
    "/login",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    summary="User Login",
    description="Authenticates user credentials and returns a JWT access token.",
)
async def login(
    login_data: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> Token:
    """
    User login endpoint.
    """
    try:
        return await auth_service.authenticate_user(login_data)
    except AuthenticationFailedException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message,
        )
