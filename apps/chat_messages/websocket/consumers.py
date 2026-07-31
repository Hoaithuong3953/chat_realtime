from core.websocket.base_consumer import BaseConsumer
from core.websocket.context import WebSocketContext
from apps.chat_messages.websocket.events import ChatEvent
from apps.chat_messages.websocket.handlers import SendMessageHandler

class ChatConsumer(BaseConsumer):
    handlers = {
        ChatEvent.SEND_MESSAGE: SendMessageHandler(),
    }

    def build_context(self) -> WebSocketContext:
        print(
            "WS USER:",
            self.scope["user"],
            self.scope["user"].id,
        )
        return WebSocketContext(
            user=self.scope["user"],
            chat_id=self.scope["url_route"]["kwargs"]["chat_id"],
        )