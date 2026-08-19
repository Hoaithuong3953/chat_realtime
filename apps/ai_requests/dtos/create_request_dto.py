from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict

from apps.ai_requests.enums import AIRequestStatus

class CreateAIRequestRequest(BaseModel):
    """Request DTO for create an AI request"""
    model_config = ConfigDict(frozen=True)
    message_id: UUID = Field(description="The message contains an AI request")

class CreateAIRequestResponse(BaseModel):
    """Response DTO return successfully create an AI request"""
    model_config = ConfigDict(frozen=True)
    
    id: UUID = Field(description="The ID of AI request")
    status: AIRequestStatus = Field(description="The processing status of AI request")