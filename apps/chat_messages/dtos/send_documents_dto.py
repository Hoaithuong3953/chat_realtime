from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

class SendDocumentsRequest(BaseModel):
    """Request DTO for sending document message"""
    model_config = ConfigDict(frozen=True)

    chat_id: UUID = Field(description="ID of the target chat")
    file_ids: list[UUID] = Field(
        description="List of uploaded file IDs to send as document messages"
    )
    text_content: str | None = Field(
        default=None,
        description="The message content is sent following to the document"
    )

class DocumentItemResponse(BaseModel):
    """Information about a sent document"""
    model_config = ConfigDict(frozen=True)

    id: UUID = Field(description="The ID of the document message")
    original_name: str = Field(description="The original filename")
    file_size: int = Field(description="The size of file")

class SendDocumentsResponse(BaseModel):
    """Response DTO returned after successfully sending document messages"""
    model_config = ConfigDict(frozen=True)

    items: list[DocumentItemResponse] = Field(
        description="List of sent document messages"
    )