from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

from apps.chats.enums import ChatType

class CreatePrivateChatRequest(BaseModel):
    """Request DTO for creating a private chat"""
    model_config = ConfigDict(frozen=True)

    target_user_id: UUID = Field(description="The user ID selected to start the conversation")

class CreatePrivateChatResponse(BaseModel):
    """Response DTO return after creating a private chat"""
    model_config = ConfigDict(frozen=True, from_attributes=True)

    chat_id: UUID = Field(description="ID of the recently created conversation")
    type: ChatType = Field(description="Type of conversation (PRIVATE)")
    created: bool = Field(description="Specifies whether the conversation has already been created (true: Yes, false: No)")