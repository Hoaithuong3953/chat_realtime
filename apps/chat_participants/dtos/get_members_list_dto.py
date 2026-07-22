from uuid import UUID
from pydantic import ConfigDict, Field, BaseModel, HttpUrl

from apps.chat_participants.enums import ParticipantRole

class MemberItemResponse(BaseModel):
    """Member information returned in the chat list"""
    model_config = ConfigDict(from_attributes=True, frozen=True)

    id: UUID = Field(description="User identification")
    full_name: str = Field(description="User's display name")
    avatar_url: HttpUrl | None = Field(description="The url of user's avatar")
    role: ParticipantRole = Field(description="User role in the chat")

class GetMembersListResponse(BaseModel):
    """Response DTO return after successfully retrieving the list of chat group members"""
    chat_id: UUID = Field(description="Retrieved chat ID")
    members: list[MemberItemResponse] = Field(description="List of members from the retrieved group chat")