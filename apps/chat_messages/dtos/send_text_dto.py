from uuid import UUID
from pydantic import Field, BaseModel, ConfigDict

from apps.chat_messages.dtos.message_dto import MessageResponse

class SendTextMessageRequest(BaseModel):
    model_config=ConfigDict(frozen=True)

    text_content: str = Field(description="The content of the message")
    reply_to_message: UUID | None = Field(default=None, description="ID of the replied message")

class SendTextMessageResponse(BaseModel):
    """Response DTO return successfully send text message to a chat"""
    model_config=ConfigDict(frozen=True)

    user_message: MessageResponse = Field(description="The content of user text message")
    ai_message: MessageResponse | None = Field(default=None, description="The content of AI service message")