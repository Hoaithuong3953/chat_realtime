from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, HttpUrl

class GetGroupChatResponse(BaseModel):
    """Response DTO return after get group chat successfully"""
    model_config = ConfigDict(from_attributes=True, frozen=True)

    chat_id: UUID = Field(description="ID of the recently created chat")
    title: str = Field(description="Title for group chat")
    avatar_url: HttpUrl | None = Field(description="The url of group chat")
    owner_id: UUID = Field(description="ID of the person who created the chat group")
    member_count: int = Field(description="The number of members in the newly created chat")
    created_at: datetime = Field(description="The time the chat group was created")