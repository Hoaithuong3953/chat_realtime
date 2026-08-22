from pydantic import BaseModel, Field, ConfigDict

from apps.chat_messages.dtos.message_dto import MessageResponse

class SendAIRequestRequest(BaseModel):
    """Request DTO for send user request to AI service"""
    model_config = ConfigDict(frozen=True)
    user_message: MessageResponse = Field(description="The content message of user")

class AITextMessageResponse(BaseModel):
    """Response DTO return successfully when AI service return response to the chat"""
    model_config=ConfigDict(frozen=True)
    message: MessageResponse | None = Field(default=None, description="The response message of AI service")