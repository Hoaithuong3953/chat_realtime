from pydantic import BaseModel, Field

from apps.users.constants import (
    PASSWORD_MIN_LENGTH,
    IDENTIFIER_MIN_LENGTH,
)

class LoginRequest(BaseModel):
    """Request DTO for user authentication"""
    identifier: str = Field(min_length=IDENTIFIER_MIN_LENGTH, description="Username or email address")
    password: str = Field(min_length=PASSWORD_MIN_LENGTH, description="The user's password")

class LoginResponse:
    """Response DTO return after successful authentication"""
    access_token: str = Field(description="JWT access token")
    refresh_token: str = Field(description="JWT refresh token")

    class Config:
        from_attributes = True