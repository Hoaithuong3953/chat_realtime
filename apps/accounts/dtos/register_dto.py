from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from apps.accounts.enums import Role

class RegisterRequest(BaseModel):
    """Request DTO for user registration"""
    model_config = ConfigDict(frozen=True)

    email: EmailStr = Field(description="The user's email address")
    username: str = Field(description="The user's username")
    password: str = Field(description="The user's password")
    full_name: str = Field(description="The name user want to display")

class RegisterResponse(BaseModel):
    """Response DTO return after successful user registration"""
    model_config = ConfigDict(from_attributes=True, frozen=True)
    
    id: UUID = Field(description="Unique user account ID")
    email: EmailStr = Field(description="The registered email address")
    username: str = Field(description="The registered username")
    full_name: str = Field(description="The registered name")
    role: Role = Field(description="The role of user account (USER, ADMIN)")
    is_active: bool = Field(description="Status of user account")
    created_at: datetime = Field(description="User account creation time")