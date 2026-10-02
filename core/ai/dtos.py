from pydantic import Field, ConfigDict, BaseModel

class AIProviderRequest(BaseModel):
    """Request DTO to receive responses from AI service"""
    model_config=ConfigDict(frozen=True)

    instruction: str | None = Field(default=None, description="Instruction that defines how the AI responses")
    input: str = Field(description="Input content provided to the AI model")

class AIProviderResponse(BaseModel):
    """Response DTO return after successfully get AI service response"""
    model_config=ConfigDict(frozen=True)

    content: str = Field(description="Generated content returned by the AI model")
    model: str = Field(description="Model used to generate the response")

class EmbeddingProviderRequest(BaseModel):
    """Request DTO to embedding request from AI service"""
    model_config = ConfigDict(frozen=True)

    input: str = Field(description="Text content to generate embedding for")

class EmbeddingProviderResponse(BaseModel):
    """Response DTO return after successfully embedding request"""
    model_config = ConfigDict(frozen=True)

    embedding: list[float] = Field(description="Generated embedding vector")
    model: str = Field(description="Embedding model used")