from uuid import UUID
from pydantic import Field, BaseModel, ConfigDict

from apps.chat_messages.dtos.message_dto import MessageResponse

class SendTextMessageRequest(BaseModel):
    """Request DTO for send text message"""
    model_config=ConfigDict(frozen=True)

    text_content: str = Field(description="The content of the message")
    reply_to_message: UUID | None = Field(default=None, description="ID of the replied message")

class SendTextMessageResponse(BaseModel):
    """Response DTO return successfully when send text message to a chat"""
    model_config=ConfigDict(frozen=True)
    message: MessageResponse = Field(description="The content of text message")