from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

class UpdateAccountResponse(BaseModel):
    """Response DTO return after successfully update account"""
    model_config = ConfigDict(frozen=True)

    id: UUID = Field(description="Account ID")
    is_active: bool = Field(description="Updated account active status")