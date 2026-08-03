import uuid
from datetime import datetime, timezone
import pytest
from httpx import AsyncClient
from app.services.user import UserService
from app.exceptions.user import EmailAlreadyExistsException
from app.models.user import User


@pytest.mark.asyncio
async def test_signup_success(client, monkeypatch):
    mock_user = User(
        id=uuid.uuid4(),
        email="test@example.com",
        first_name="John",
        last_name="Doe",
        role="employee",
        is_active=True,
        is_email_verified=False,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    
    async def mock_register_user(self, user_in):
        return mock_user
        
    monkeypatch.setattr(UserService, "register_user", mock_register_user)

    response = await client.post(
        "/api/v1/auth/signup",
        json={
            "email": "test@example.com",
            "password": "securepassword123",
            "first_name": "John",
            "last_name": "Doe"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["first_name"] == "John"
    assert data["last_name"] == "Doe"
    assert "password" not in data


@pytest.mark.asyncio
async def test_signup_duplicate_email(client, monkeypatch):
    async def mock_register_user(self, user_in):
        raise EmailAlreadyExistsException(user_in.email)
        
    monkeypatch.setattr(UserService, "register_user", mock_register_user)

    response = await client.post(
        "/api/v1/auth/signup",
        json={
            "email": "existing@example.com",
            "password": "securepassword123",
        }
    )
    assert response.status_code == 409
    assert response.json()["detail"] == "User with email 'existing@example.com' already exists."


@pytest.mark.asyncio
async def test_signup_invalid_email(client):
    response = await client.post(
        "/api/v1/auth/signup",
        json={
            "email": "invalid-email",
            "password": "securepassword123",
        }
    )
    assert response.status_code == 422
