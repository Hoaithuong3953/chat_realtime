from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

from apps.chat_messages.enums import MessageType

class FileResponse(BaseModel):
    """Information about a sent file"""
    model_config = ConfigDict(frozen=True)

    file_asset_id: UUID = Field(description="ID of the uploaded file asset")
    original_name: str = Field(description="The original filename")
    file_size: int = Field(description="The size of file in bytes")

class MessageResponse(BaseModel):
    """Information about a message"""
    model_config=ConfigDict(frozen=True)

    id: UUID = Field(description="ID of the message")
    chat: UUID = Field(description="ID of chat containing the message")
    user: UUID | None = Field(description="ID of the sender")
    message_type: MessageType = Field(description="Type of message sent")
    text_content: str | None = Field(default=None, description="Text content of the message, if applicable")
    file: FileResponse | None = Field(default=None, description="File information if the message is a file message")
    reply_to_message: UUID | None = Field(default=None, description="ID of the replied message")
    created_at: datetime = Field(description="The time the message was sent")
    recalled_at: datetime | None = Field(default=None, description="The time the message was recalled")