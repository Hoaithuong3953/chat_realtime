from datetime import datetime
from uuid import UUID
from pydantic import Field, BaseModel, ConfigDict

from apps.chat_messages.enums import MessageType

class SendMessageRequest(BaseModel):
    model_config=ConfigDict(frozen=True)

    text_content: str = Field(description="The content of the message")
    reply_to_message: UUID | None = Field(default=None, description="ID of the replied message")

class SendMessageResponse(BaseModel):
    model_config=ConfigDict(frozen=True, from_attributes=True)

    id: UUID = Field(description="ID of the recently sent message")
    chat: UUID = Field(description="Chat ID containing the message")
    user: UUID = Field(description="ID of the sender")
    message_type: MessageType = Field(description="Type of message sent")
    text_content: str = Field(description="The content of the message")
    reply_to_message: UUID | None = Field(description="ID of the replied message")
    created_at: datetime = Field(description="The time the message was sent")