from pydantic import BaseModel, ConfigDict, Field

class LoginRequest(BaseModel):
    """Request DTO for user authentication"""
    model_config = ConfigDict(frozen=True)

    identifier: str = Field(description="Username or email address")
    password: str = Field(description="The user's password")

class LoginResponse(BaseModel):
    """Response DTO return after successful authentication"""
    model_config = ConfigDict(from_attributes=True, frozen=True)
    
    access_token: str = Field(description="JWT access token")
    refresh_token: str = Field(description="JWT refresh token")