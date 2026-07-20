from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, HttpUrl

class UpdateGroupChatRequest(BaseModel):
    """Request DTO for updating a group chat information"""
    model_config = ConfigDict(frozen=True)

    title: str = Field(description="Title for group chat")
    avatar_url: HttpUrl | None = Field(default=None, description="The url of group chat")

class UpdateGroupChatResponse(BaseModel):
    """Response DTO after creating group chat successfully"""
    model_config = ConfigDict(from_attributes=True, frozen=True)

    id: UUID = Field(description="ID of the recently created chat")
    title: str = Field(description="Title for group chat")
    avatar_url: HttpUrl | None = Field(description="The url of group chat")
    updated_at: datetime = Field(description="The time the group chat was updated")