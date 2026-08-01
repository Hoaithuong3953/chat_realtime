from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async

from core.websocket.base_consumer import BaseConsumer
from core.websocket.context import WebSocketContext
from apps.chat_messages.websocket.events import ChatEvent
from apps.chat_messages.websocket.handlers import SendMessageHandler
from apps.chat_messages.websocket.connect_service import ChatConnectService
from apps.chat_messages.exceptions import ChatAccessDeniedException, ChatNotFoundException

class ChatConsumer(BaseConsumer):
    group_name: str | None = None

    handlers = {
        ChatEvent.SEND_MESSAGE: SendMessageHandler(),
    }

    def build_context(self) -> WebSocketContext:
        """Build the context for the WebSocket connection"""
        return WebSocketContext(
            user=self.scope["user"],
            chat_id=self.scope["url_route"]["kwargs"]["chat_id"],
        )

    async def connect(self) -> None:
        """Handle the WebSocket connection"""
        user = self.scope["user"]
        if isinstance(user, AnonymousUser):
            await self.close(code=401)

        chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
        try:
            await database_sync_to_async(
                ChatConnectService.validate_chat
            )(
                chat_id=chat_id,
                user_id=user.id,
            )

        except ChatNotFoundException:
            await self.close(code=404)
            return
        except ChatAccessDeniedException:
            await self.close(code=403)
            return

        self.group_name = f"chat_{chat_id}"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name,
        )
        await self.accept()

    async def disconnect(self, code: int) -> None:
        """Handle the WebSocket disconnection"""
        if self.group_name is not None:
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name,
            )

    async def after_handle(self, response):
        """Perform actions after handling send message event"""
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
        """Receive a message from the group and send it to the WebSocket"""
        await self.send_json(event["message"])