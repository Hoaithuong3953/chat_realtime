from dataclasses import dataclass
from pydantic import BaseModel, ConfigDict, Field

from apps.users.constants import (
    PASSWORD_MIN_LENGTH,
    IDENTIFIER_MIN_LENGTH,
)

@dataclass(frozen=True)
class LoginRequest(BaseModel):
    """Request DTO for user authentication"""
    identifier: str = Field(min_length=IDENTIFIER_MIN_LENGTH, description="Username or email address")
    password: str = Field(min_length=PASSWORD_MIN_LENGTH, description="The user's password")

@dataclass(frozen=True)
class LoginResponse(BaseModel):
    """Response DTO return after successful authentication"""
    model_config = ConfigDict(from_attributes=True)
    
    access_token: str = Field(description="JWT access token")
    refresh_token: str = Field(description="JWT refresh token")