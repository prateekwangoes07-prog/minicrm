from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies.user import get_user_service
from app.exceptions.user import EmailAlreadyExistsException
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.services.user import UserService

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
