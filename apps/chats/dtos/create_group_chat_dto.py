from uuid import UUID
from pydantic import Field, BaseModel, ConfigDict

from apps.chats.enums import ChatType

class CreateGroupChatRequest(BaseModel):
    """Request DTO for creating a group chat"""
    model_config = ConfigDict(frozen=True)

    title: str = Field(description="Title for group chat")
    member_ids: list[UUID] = Field(description="List of user IDs for group chat")

class CreateGroupChatResponse(BaseModel):
    """Response DTO return after creating group chat successfully"""
    model_config = ConfigDict(from_attributes=True, frozen=True)

    chat_id: UUID = Field(description="ID of the recently created chat")
    type: ChatType = Field(description="Type of chat (GROUP)")
    title: str = Field(description="Title of group chat")
    member_count: int = Field(description="Total number of participants in group")