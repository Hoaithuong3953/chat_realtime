from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict

class AddGroupMembersRequest(BaseModel):
    """Request DTO for adding members to the group chat"""
    model_config = ConfigDict(frozen=True)

    member_ids: list[UUID] = Field(description="List of user IDs to add to the chat")

class AddGroupMembersResponse(BaseModel):
    """Response DTO return after successfully adding members to the group chat"""
    model_config = ConfigDict(from_attributes=True, frozen=True)

    id: UUID = Field(description="The target chat ID")
    member_count: int = Field(description="Number of members to add to the chat")