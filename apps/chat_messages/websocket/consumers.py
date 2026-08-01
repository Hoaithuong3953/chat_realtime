from core.websocket.base_consumer import BaseConsumer
from core.websocket.context import WebSocketContext
from apps.chat_messages.websocket.events import ChatEvent
from apps.chat_messages.websocket.handlers import SendMessageHandler

class ChatConsumer(BaseConsumer):
    handlers = {
        ChatEvent.SEND_MESSAGE: SendMessageHandler(),
    }

    def build_context(self) -> WebSocketContext:
        return WebSocketContext(
            user=self.scope["user"],
            chat_id=self.scope["url_route"]["kwargs"]["chat_id"],
        )

    async def connect(self) -> None:
        self.group_name = f"chat_{self.scope['url_route']['kwargs']['chat_id']}"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name,
        )
        await self.accept()

    async def disconnect(self, code: int) -> None:
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name,
        )

    async def after_handle(self, response):
        if response.event != ChatEvent.SEND_MESSAGE:
            return False

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat.message",
                "message": response.model_dump(mode="json")
            },
        )

        return True

    async def chat_message(self, event: dict) -> None:
        await self.send_json(event["message"])