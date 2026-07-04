from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from datetime import datetime

from apps.users.constants import (
    NAME_MAX_LENGTH,
    NAME_MIN_LENGTH,
    PASSWORD_MIN_LENGTH,
    USERNAME_MAX_LENGTH,
    USERNAME_MIN_LENGTH,
)

class RegisterRequest(BaseModel):
    """
    Immutable data class representing a user registration request
    """
    email: EmailStr = Field(description="The user's email address")
    username: str = Field(min_length=USERNAME_MIN_LENGTH, max_length=USERNAME_MAX_LENGTH, description="The user's username")
    password: str = Field(min_length=PASSWORD_MIN_LENGTH, description="The user's password")
    name: str = Field(min_length=NAME_MIN_LENGTH, max_length=NAME_MAX_LENGTH, description="The name user want to display")

class RegisterResponse(BaseModel):
    """
    Immutable data class representing the response after successful user registration
    """
    id: UUID = Field(description="Unique user account ID")
    email: EmailStr = Field(description="The registered email address")
    username: str = Field(description="The registered username")
    name: str = Field(description="The registered name")
    role: str = Field(description="The role of user account (USER, ADMIN)")
    is_active: bool = Field(description="Status of user account")
    created_at: datetime = Field(description="User account creation time")

    class Config:
        from_attributes = True