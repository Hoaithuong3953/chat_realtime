from dataclasses import dataclass
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from uuid import UUID
from datetime import datetime

from apps.users.constants import (
    NAME_MAX_LENGTH,
    NAME_MIN_LENGTH,
    PASSWORD_MIN_LENGTH,
    USERNAME_MAX_LENGTH,
    USERNAME_MIN_LENGTH,
)

@dataclass(frozen=True)
class RegisterRequest(BaseModel):
    """Request DTO for user registration"""
    email: EmailStr = Field(description="The user's email address")
    username: str = Field(min_length=USERNAME_MIN_LENGTH, max_length=USERNAME_MAX_LENGTH, description="The user's username")
    password: str = Field(min_length=PASSWORD_MIN_LENGTH, description="The user's password")
    name: str = Field(min_length=NAME_MIN_LENGTH, max_length=NAME_MAX_LENGTH, description="The name user want to display")

@dataclass(frozen=True)
class RegisterResponse(BaseModel):
    """Response DTO return after successful user registration"""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID = Field(description="Unique user account ID")
    email: EmailStr = Field(description="The registered email address")
    username: str = Field(description="The registered username")
    name: str = Field(description="The registered name")
    role: str = Field(description="The role of user account (USER, ADMIN)")
    is_active: bool = Field(description="Status of user account")
    created_at: datetime = Field(description="User account creation time")