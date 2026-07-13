from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from apps.accounts.enums import Role

class MeResponse(BaseModel):
    """Response DTO return after successful get current user infomation"""
    model_config = ConfigDict(from_attributes=True, frozen=True)
    
    id: UUID = Field(description="Unique user account ID")
    email: EmailStr = Field(description="The email address")
    username: str = Field(description="The username")
    full_name: str = Field(description="The display name")
    role: Role = Field(description="The role of user account (USER, ADMIN)")
    is_active: bool = Field(description="Status of user account")
    created_at: datetime = Field(description="User account creation time")