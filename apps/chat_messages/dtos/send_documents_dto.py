from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

from apps.chat_messages.dtos.message_dto import MessageResponse

class SendDocumentMessageRequest(BaseModel):
    """Request DTO for sending document message"""
    model_config = ConfigDict(frozen=True)

    file_ids: list[UUID] = Field(
        description="List of uploaded file IDs to send as document messages"
    )
    text_content: str | None = Field(
        default=None,
        description="Optional text message sent together with the documents"
    )
    reply_to_message: UUID | None = Field(
        default=None,
        description="ID of the message being replied to"
    )

class SendDocumentMessageResponse(BaseModel):
    """Response DTO return successfully send document message to a chat"""
    model_config=ConfigDict(frozen=True)
    messages: list[MessageResponse] = Field(
        description="List of created messages, including the optional text message and document messages"
    )