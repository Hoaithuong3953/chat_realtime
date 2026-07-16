from uuid import UUID
from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, Field, HttpUrl

class UpdateProfileRequest(BaseModel):
    """Request DTO for update user profile information"""
    model_config = ConfigDict(frozen=True)

    full_name: str | None = Field(default=None, description="User's display name")
    avatar_url: HttpUrl | None = Field(default=None, description="The url of user's avatar")
    phone_number: str | None = Field(default=None, description="User's phone number")
    address: str | None = Field(default=None, description="User's address")
    dob: date | None = Field(default=None, description="User's date of birth")
    bio: str | None = Field(default=None, description="User bio")

class UpdateProfileResponse(BaseModel):
    """Response DTO return after successful get user profile information"""
    model_config = ConfigDict(from_attributes=True, frozen=True)

    id: UUID = Field(description="User identification")
    full_name: str = Field(description="User's display name")
    avatar_url: HttpUrl | None = Field(description="The url of user's avatar")
    phone_number: str | None = Field(description="User's phone number")
    address: str | None = Field(description="User's address")
    dob: date | None = Field(description="User's date of birth")
    bio: str | None = Field(description="User bio")
    updated_at: datetime = Field(description="User profile update time")