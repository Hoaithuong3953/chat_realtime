from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

from apps.chat_messages.enums import MessageStatus

class RecallMessageResponse(BaseModel):
    model_config=ConfigDict(frozen=True, from_attributes=True)

    id: UUID = Field(description="The identifier of the recalled message")
    status: MessageStatus = Field(description="Current message status")
    recalled_at: datetime = Field(description="The time that message was recalled")