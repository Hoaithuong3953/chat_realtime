from datetime import datetime
from uuid import UUID
from pydantic import Field, BaseModel, ConfigDict

from apps.chat_messages.enums import MessageType

class SendTextMessageRequest(BaseModel):
    model_config=ConfigDict(frozen=True)

    text_content: str = Field(description="The content of the message")
    reply_to_message: UUID | None = Field(default=None, description="ID of the replied message")

class SendTextMessageResponse(BaseModel):
    """Response DTO return successfully send text message to a chat"""
    model_config=ConfigDict(frozen=True)

    id: UUID = Field(description="ID of the message")
    chat: UUID = Field(description="ID of chat containing the message")
    user: UUID = Field(description="ID of the sender")
    message_type: MessageType = Field(description="Type of message sent")
    text_content: str | None = Field(default=None, description="Text content of the message, if applicable")
    reply_to_message: UUID | None = Field(default=None, description="ID of the replied message")
    created_at: datetime = Field(description="The time the message was sent")