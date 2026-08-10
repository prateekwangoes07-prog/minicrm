from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field


class CustomerBase(BaseModel):
    first_name: str = Field(..., max_length=255)
    last_name: str = Field(..., max_length=255)
    email: EmailStr
    phone: str | None = Field(default=None, max_length=20)
    address: str | None = Field(default=None)
    notes: str | None = Field(default=None)


class CustomerCreate(CustomerBase):
    company_id: UUID


class CustomerUpdate(BaseModel):
    first_name: str | None = Field(default=None, max_length=255)
    last_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None)
    phone: str | None = Field(default=None, max_length=20)
    address: str | None = Field(default=None)
    notes: str | None = Field(default=None)
    company_id: UUID | None = Field(default=None)
    is_active: bool | None = Field(default=None)


class CustomerResponse(CustomerBase):
    id: UUID
    company_id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }
