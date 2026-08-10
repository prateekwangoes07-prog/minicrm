from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field


class EmployeeBase(BaseModel):
    email: EmailStr
    first_name: str | None = Field(default=None, max_length=255)
    last_name: str | None = Field(default=None, max_length=255)


class EmployeeCreate(EmployeeBase):
    password: str = Field(..., min_length=8, max_length=100)
    company_id: UUID


class EmployeeUpdate(BaseModel):
    email: EmailStr | None = Field(default=None)
    first_name: str | None = Field(default=None, max_length=255)
    last_name: str | None = Field(default=None, max_length=255)
    password: str | None = Field(default=None, min_length=8, max_length=100)
    company_id: UUID | None = Field(default=None)
    is_active: bool | None = Field(default=None)


class EmployeeResponse(EmployeeBase):
    id: UUID
    role: str
    is_active: bool
    is_email_verified: bool
    company_id: UUID | None
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }
