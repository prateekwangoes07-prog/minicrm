from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field


class CompanyBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr = Field(..., max_length=255)
    phone: str | None = Field(default=None, max_length=20)
    address: str | None = Field(default=None)
    website_url: str | None = Field(default=None, max_length=255)
    industry: str | None = Field(default=None, max_length=100)


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)
    phone: str | None = Field(default=None, max_length=20)
    address: str | None = Field(default=None)
    website_url: str | None = Field(default=None, max_length=255)
    industry: str | None = Field(default=None, max_length=100)
    is_active: bool | None = Field(default=None)


class CompanyResponse(CompanyBase):
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }
