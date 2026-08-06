from pydantic import BaseModel, ConfigDict, Field

from apps.chat_messages.dtos.message_dto import MessageResponse

class GetChatHistoryRequest(BaseModel):
    """Request DTO for get chat history"""
    model_config=ConfigDict(frozen=True)

    before: str | None = Field(default=None, description="Previous page's cursor")
    limit: int = Field(description="Number of messages to retrieve")

class PaginationResponse(BaseModel):
    """Pagination metadata for get chat history"""
    model_config=ConfigDict(frozen=True)

    has_next: bool = Field(description="Check if exist older message")
    next_cursor: str | None = Field(default=None, description="Cursor for the next load")

class GetChatHistoryResponse(BaseModel):
    """Response DTO for display chat message list"""
    messages: list[MessageResponse] = Field(description="List of messages in a chat")
    pagination: PaginationResponse = Field(description="Pagination metadata for loading older messages")