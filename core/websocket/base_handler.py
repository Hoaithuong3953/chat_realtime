from typing import Protocol

from core.websocket.context import WebSocketContext
from backend.core.websocket.base_schema import WebSocketRequest, WebSocketResponse

class WebSocketHandler(Protocol):
    async def handle(
        self,
        context: WebSocketContext,
        request: WebSocketRequest,
    ) -> WebSocketResponse:
        """Process a websocket event"""
        ...