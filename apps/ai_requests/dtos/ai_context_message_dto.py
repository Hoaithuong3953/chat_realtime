from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

from apps.chat_messages.enums import MessageType, SenderType

class AIContextMessage(BaseModel):
    """Message DTO used for building AI context"""
    model_config = ConfigDict(frozen=True)

    id: UUID = Field(description="ID of the message")
    message_type: MessageType = Field(description="Type of the message")
    sender_type: SenderType = Field(description="Type of sender")
    full_name: str | None = Field(
        default=None,
        description="Full name of the user who sent the message",
    )
    text_content: str | None = Field(
        default=None,
        description="Text content of the message",
    )