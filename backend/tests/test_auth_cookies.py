import uuid
import pytest
from datetime import datetime, timezone
from app.main import app
from app.models.user import User
from app.dependencies.auth import get_current_user
from app.services.auth import AuthService
from app.schemas.token import Token


mock_user = User(
    id=uuid.uuid4(),
    email="test@user.com",
    role="employee",
    is_active=True,
    is_email_verified=True,
    created_at=datetime.now(timezone.utc),
    updated_at=datetime.now(timezone.utc),
)



@pytest.fixture(autouse=True)
def clean_overrides():
    app.dependency_overrides.clear()
    yield
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_login_sets_cookie_and_me_works(client, monkeypatch):
    """
    Test that login correctly sets the access_token cookie,
    and GET /auth/me extracts user details successfully.
    """
    # Mock authentication token return
    mock_token = Token(access_token="mock_jwt_token", token_type="bearer")
    async def mock_authenticate(self, login_data):
        return mock_token

    monkeypatch.setattr(AuthService, "authenticate_user", mock_authenticate)

    # 1. Login to set cookie
    login_response = await client.post(
        "/api/v1/auth/login",
        json={"email": "test@user.com", "password": "password123"},
    )
    assert login_response.status_code == 200
    assert "access_token" in login_response.cookies

    # Mock token verification so it returns mock_user.id
    monkeypatch.setattr("app.dependencies.auth.verify_access_token", lambda tok: str(mock_user.id))
    
    # Mock DB user fetching in AuthRepository
    from app.repositories.auth import AuthRepository
    async def mock_get_user_by_id(self, user_id):
        return mock_user
    monkeypatch.setattr(AuthRepository, "get_user_by_id", mock_get_user_by_id)

    # 2. Call GET /auth/me using the cookie
    me_response = await client.get("/api/v1/auth/me")
    assert me_response.status_code == 200
    assert me_response.json()["email"] == "test@user.com"

    # 3. Logout to delete cookie
    logout_response = await client.post("/api/v1/auth/logout")
    assert logout_response.status_code == 200
    assert client.cookies.get("access_token") in (None, "")
