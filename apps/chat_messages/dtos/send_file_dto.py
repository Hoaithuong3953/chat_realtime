from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

from apps.chat_messages.dtos.message_dto import MessageResponse

class SendFileMessageRequest(BaseModel):
    """Request DTO for sending file message"""
    model_config = ConfigDict(frozen=True)

    file_ids: list[UUID] = Field(
        description="List of uploaded file IDs to send"
    )
    text_content: str | None = Field(
        default=None,
        description="Optional text message sent together with the files"
    )
    reply_to_message: UUID | None = Field(
        default=None,
        description="ID of the message being replied to"
    )

class SendFileMessageResponse(BaseModel):
    """Response DTO return successfully send file message to a chat"""
    model_config=ConfigDict(frozen=True)
    messages: list[MessageResponse] = Field(
        description="List of created messages, including the optional text message and file messages"
    )