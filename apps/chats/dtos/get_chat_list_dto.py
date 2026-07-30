from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict, HttpUrl

from apps.chat_messages.enums import MessageType, MessageStatus
from apps.chats.enums import ChatType

class GetChatListRequest(BaseModel):
    """Request DTO for get chat list"""
    model_config=ConfigDict(frozen=True)

    before: str | None = Field(default=None, description="Previous page's cursor")
    limit: int = Field(description="Number of chat to retrieve")

class LastMessageResponse(BaseModel):
    """Return last message for a chat"""
    model_config=ConfigDict(frozen=True)

    id: UUID = Field(description="Last message ID")
    sender_id: UUID = Field(description="Sender ID")
    message_type: MessageType = Field(description="Message type")
    text_content: str | None = Field(description="Message content")
    status: MessageStatus = Field(description="Current status of the message")
    recalled_at: datetime | None = Field(description="The time that the message was recalled")
    created_at: datetime = Field(description="The time of sending message")

class ChatListItemResponse(BaseModel):
    """Chat returned in chat list"""
    model_config=ConfigDict(frozen=True)

    id: UUID = Field(description="Chat ID")
    type: ChatType = Field(description="Chat type")
    title: str | None = Field(description="Title of chat")
    avatar_url: HttpUrl | None = Field(description="Avatar URL of chat")
    last_message: LastMessageResponse | None = Field(description="Last message of the chat")
    last_activity_at: datetime = Field(description="The time of last activity")

class PaginationResponse(BaseModel):
    """Pagination metadata for get chat list"""
    model_config=ConfigDict(frozen=True)

    has_next: bool = Field(description="Check if exist older chats")
    next_cursor: str | None = Field(default=None, description="Cursor for the next load")

class GetChatListResponse(BaseModel):
    """Response DTO for display chat list"""
    items: list[ChatListItemResponse] = Field(description="List chat of the user")
    pagination: PaginationResponse = Field(description="Pagination metadata for loading older chats")