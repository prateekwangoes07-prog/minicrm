from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, field_validator

VALID_STATUSES = {"new", "contacted", "qualified", "proposal", "won", "lost"}


class LeadBase(BaseModel):
    name: str = Field(..., max_length=255)
    email: EmailStr
    phone: str | None = Field(default=None, max_length=20)
    requirement: str | None = Field(default=None)
    status: str = Field(default="new", max_length=50)
    source: str | None = Field(default=None, max_length=100)
    notes: str | None = Field(default=None)

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: str) -> str:
        if value not in VALID_STATUSES:
            raise ValueError(
                f"Invalid status. Must be one of: {', '.join(sorted(VALID_STATUSES))}"
            )
        return value


class LeadCreate(LeadBase):
    company_id: UUID
    customer_id: UUID | None = Field(default=None)
    assigned_to: UUID | None = Field(default=None)


class LeadUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None)
    phone: str | None = Field(default=None, max_length=20)
    requirement: str | None = Field(default=None)
    status: str | None = Field(default=None, max_length=50)
    source: str | None = Field(default=None, max_length=100)
    notes: str | None = Field(default=None)
    company_id: UUID | None = Field(default=None)
    customer_id: UUID | None = Field(default=None)
    assigned_to: UUID | None = Field(default=None)

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: str | None) -> str | None:
        if value is not None and value not in VALID_STATUSES:
            raise ValueError(
                f"Invalid status. Must be one of: {', '.join(sorted(VALID_STATUSES))}"
            )
        return value


class LeadResponse(LeadBase):
    id: UUID
    company_id: UUID
    customer_id: UUID | None
    assigned_to: UUID | None
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }
