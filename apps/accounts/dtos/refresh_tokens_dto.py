from pydantic import BaseModel, Field

class RefreshTokenResponse(BaseModel):
    access_token: str = Field(description="JWT access token")
    refresh_token: str = Field(description="JWT refresh token")