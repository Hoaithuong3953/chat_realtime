from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, HttpUrl

from shared.pagination_dto import PaginationResponse

class GetUsersRequest(BaseModel):
    """Request DTO for display active user list"""
    model_config = ConfigDict(frozen=True)

    q: str | None = Field(default=None, description="Search keyword for full name")
    page: int = Field(description="Current page number")
    page_size: int = Field(description="Number of users per page")

class UserItemResponse(BaseModel):
    """User information returned in user list"""
    model_config = ConfigDict(from_attributes=True, frozen=True)

    id: UUID = Field(description="User identification")
    full_name: str = Field(description="User's display name")
    avatar_url: HttpUrl | None = Field(description="The url of user's avatar")
    bio: str | None = Field(description="User bio")

class GetUsersResponse(BaseModel):
    """Response DTO for display active user list"""
    items: list[UserItemResponse] = Field(description="List of users")
    pagination: PaginationResponse = Field(description="Pagination information")