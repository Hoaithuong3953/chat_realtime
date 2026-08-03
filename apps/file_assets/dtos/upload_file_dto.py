from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

from apps.file_assets.enums import FileStatus

class UploadFileResponse(BaseModel):
    """Response DTO return after successfully upload file"""
    model_config = ConfigDict(from_attributes=True, frozen=True)

    id: UUID = Field(description="ID of the uploaded file")
    storage_key: str = Field(description="Storage key or path used to locate the file in the storage backend")
    original_name: str = Field(description="Original name of the uploaded file")
    content_type: str = Field(description="MIME type of the uploaded file")
    file_size: int = Field(description="Size of the uploaded file")
    status: FileStatus = Field(description="Current processing status of the uploaded file")
    created_at: datetime = Field(description="Timestamp when the file was uploaded")