from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict

from apps.accounts.enums import Role
from shared.pagination_dto import PaginationResponse

class GetAccountsRequest(BaseModel):
    """Request DTO for get accounts request"""
    model_config=ConfigDict(frozen=True)

    q: str | None = Field(default=None, description="Search by email, username, or full name")
    role: Role | None = Field(default=None, description="Filter accounts by role")
    is_active: bool | None = Field(default=None, description="Filter accounts by active status")
    page: int = Field(description="Page number")
    page_size: int = Field(description="Number of accounts per page")

class AccountItemResponse(BaseModel):
    """Account information returned in account list"""
    model_config=ConfigDict(frozen=True)

    id: UUID = Field(description="Account ID")
    email: str = Field(description="Account email address")
    username: str = Field(description="Account username")
    role: Role = Field(description="Account role")
    is_active: bool = Field(description="Whether the account is active")
    full_name: str = Field(description="User's full name")
    avatar_url: str | None = Field(description="User's avatar URL")

class GetAccountsResponse(BaseModel):
    """Response DTO return after successfully get account list"""
    model_config=ConfigDict(frozen=True)

    items: list[AccountItemResponse] = Field(description="List of accounts")
    pagination: PaginationResponse = Field(description="Pagination metadata")