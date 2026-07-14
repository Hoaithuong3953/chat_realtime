from uuid import UUID
from datetime import date
from pydantic import BaseModel, ConfigDict, Field, HttpUrl

class GetProfileResponse(BaseModel):
    """Response DTO return after successful get user profile information"""
    model_config = ConfigDict(from_attributes=True, frozen=True)

    id: UUID = Field(description="User identification")
    full_name: str = Field(description="User's display name")
    avatar_url: HttpUrl | None = Field(description="The url of user's avatar")
    phone_number: str | None = Field(description="User's phone number")
    address: str | None = Field(description="User's address")
    dob: date | None = Field(description="User's date of birth")
    bio: str | None = Field(description="User bio")