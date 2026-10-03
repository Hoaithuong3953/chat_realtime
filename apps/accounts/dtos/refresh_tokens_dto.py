from pydantic import BaseModel, Field, ConfigDict

class RefreshTokenResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    access_token: str = Field(description="JWT access token")
    expires_in: int = Field(description="Access token lifetime in seconds")
    refresh_token: str = Field(description="New refresh token")