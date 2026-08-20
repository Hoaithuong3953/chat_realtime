from pydantic import Field, ConfigDict, BaseModel

class AIProviderRequest(BaseModel):
    """Request DTO to receive responses from AI service"""
    model_config=ConfigDict(frozen=True)

    instruction: str = Field(description="Instruction that defines how the AI responses")
    input: str = Field(description="Input content provided to the AI model")

class AIProviderResponse(BaseModel):
    """Response DTO return after successfully get AI service response"""
    model_config=ConfigDict(frozen=True)

    content: str = Field(description="Generated content returned by the AI model")
    model: str = Field(description="Model used to generate the response")