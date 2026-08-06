from datetime import datetime
from uuid import UUID
from django.core import signing
from pydantic import BaseModel, ConfigDict

from shared.exceptions.chat.pagination import InvalidCursorException

class ChatCursorData(BaseModel):
    model_config=ConfigDict(frozen=True)
    
    last_activity_at: datetime
    chat_id: UUID

class ChatCursor:
    @staticmethod
    def encode(last_activity_at: datetime, chat_id: UUID) -> str:
        """Create a signed cursor from a chat position"""
        payload = {
            "last_activity_at": last_activity_at.isoformat(),
            "id": str(chat_id),
        }

        return signing.dumps(payload)

    @staticmethod
    def decode(cursor: str | None) -> ChatCursorData:
        """Decode and verify a signed cursor"""
        try:
            payload = signing.loads(cursor)
        except signing.BadSignature as exc:
            raise InvalidCursorException() from exc

        return ChatCursorData(
            last_activity_at=datetime.fromisoformat(payload["last_activity_at"]),
            chat_id=UUID(payload["id"]),
        )