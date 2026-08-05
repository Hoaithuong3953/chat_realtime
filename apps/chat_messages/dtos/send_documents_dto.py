from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

from apps.chat_messages.enums import MessageType

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

class DocumentResponse(BaseModel):
    """Information about a sent document"""
    model_config = ConfigDict(frozen=True)

    file_asset_id: UUID = Field(description="ID of the uploaded file asset")
    original_name: str = Field(description="The original filename")
    file_size: int = Field(description="The size of file in bytes")

class MessageResponse(BaseModel):
    """Information about a message"""
    model_config=ConfigDict(frozen=True)

    id: UUID = Field(description="ID of the message")
    chat: UUID = Field(description="ID of chat containing the message")
    user: UUID = Field(description="ID of the sender")
    message_type: MessageType = Field(description="Type of message sent")
    text_content: str | None = Field(default=None, description="Text content of the message, if applicable")
    document: DocumentResponse | None = Field(default=None, description="Document information if the message is a document message")
    reply_to_message: UUID | None = Field(default=None, description="ID of the replied message")
    created_at: datetime = Field(description="The time the message was sent")

class SendDocumentMessageResponse(BaseModel):
    """Response DTO return successfully send message to a chat (for document message)"""
    model_config=ConfigDict(frozen=True)
    messages: list[MessageResponse] = Field(
        description="List of created messages, including the optional text message and document messages"
    )