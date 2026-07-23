from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict

class TransferOwnershipRequest(BaseModel):
    """Request DTO for transferring permission owner to another member"""
    model_config = ConfigDict(frozen=True)
    
    new_owner_id: UUID = Field(description="ID of the new group owner")