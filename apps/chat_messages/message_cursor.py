from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from django.core import signing

from apps.chat_messages.exceptions import InvalidCursorException

@dataclass(frozen=True)
class MessageCursorData:
    created_at: datetime
    message_id: UUID

class MessageCursor:
    @staticmethod
    def encode(created_at: datetime, message_id: UUID) -> str:
        """Create a signed cursor from a message position"""
        payload = {
            "created_at": created_at.isoformat(),
            "id": str(message_id),
        }

        return signing.dumps(payload)

    @staticmethod
    def decode(cursor: str | None) -> MessageCursorData:
        """Decode and verify a signed cursor"""
        try:
            payload = signing.loads(cursor)
        except signing.BadSignature as exc:
            raise InvalidCursorException() from exc

        return MessageCursorData(
            created_at=datetime.fromisoformat(payload["created_at"]),
            message_id=UUID(payload["id"]),
        )