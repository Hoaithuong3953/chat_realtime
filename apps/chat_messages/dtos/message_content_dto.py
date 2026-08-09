from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

class DocumentResponse(BaseModel):
    """Information about a sent document"""
    model_config = ConfigDict(frozen=True)

    file_asset_id: UUID = Field(description="ID of the uploaded file asset")
    original_name: str = Field(description="The original filename")
    file_size: int = Field(description="The size of file in bytes")

class ImageResponse(BaseModel):
    """Information about a sent image"""
    model_config = ConfigDict(frozen=True)

    id: UUID = Field(description="ID of the message image")
    asset_id: UUID = Field(description="ID of the uploaded file asset")
    position: int = Field(description="Position of the image within the message, starting from 0")