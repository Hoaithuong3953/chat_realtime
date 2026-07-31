from dataclasses import dataclass
from uuid import UUID

from apps.users.models import User

@dataclass(slots=True)
class WebSocketContext:
    """
    Carries transport-related information from the WebSocket layer into business handlers
    """
    user: User
    chat_id: UUID
    channel_name: str