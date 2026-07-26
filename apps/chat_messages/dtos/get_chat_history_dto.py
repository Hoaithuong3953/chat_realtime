from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

from apps.chat_messages.enums import MessageType

class GetChatHistoryRequest(BaseModel):
    """Request DTO for get chat history"""
    model_config=ConfigDict(frozen=True)

    before: str | None = Field(default=None, description="Previous page's cursor")
    limit: int = Field(description="Number of messages to retrieve")

class MessageItemResponse(BaseModel):
    """Chat history returned in message list"""
    model_config=ConfigDict(frozen=True)

    id: UUID = Field(description="Message ID")
    chat_id: UUID = Field(description="Chat ID")
    sender_id: UUID = Field(description="Sender ID")
    content: str = Field(description="Message content")
    message_type: MessageType = Field(description="Message type")
    created_at: datetime = Field(description="The time of sending message")

class PaginationResponse(BaseModel):
    """Pagination metadata for get chat history"""
    model_config=ConfigDict(frozen=True)

    has_next: bool = Field(description="Check if exist older message")
    next_cursor: str | None = Field(default=None, description="Cursor for the next load")

class GetChatHistoryResponse(BaseModel):
    """Response DTO for display chat message list"""
    items: list[MessageItemResponse] = Field(description="List of message in a chat")
    pagination: PaginationResponse = Field(description="Pagination metadata for loading older messages")