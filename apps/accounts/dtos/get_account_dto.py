from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

from apps.accounts.enums import Role

class GetAccountResponse(BaseModel):
    """Response DTO return after successfully get account information"""
    model_config = ConfigDict(frozen=True)
    
    id: UUID = Field(description="Account ID")
    email: str = Field(description="Account email")
    username: str = Field(description="Account username")
    role: Role = Field(description="Account role")
    is_active: bool = Field(description="Account active status")
    full_name: str = Field(description="User full name")
    avatar_url: str | None = Field(description="User avatar URL")
    created_at: datetime = Field(description="Account creation time")
    updated_at: datetime = Field(description="Account last update time")