from channels.db import database_sync_to_async

from core.websocket.context import WebSocketContext
from core.websocket.base_handler import WebSocketHandler
from core.websocket.base_schema import WebSocketRequest, WebSocketResponse

from apps.chat_messages.services import TextMessageService
from apps.chat_messages.dtos import SendMessageRequest
from apps.chat_messages.websocket.events import ChatEvent

class SendMessageHandler(WebSocketHandler):
    event = ChatEvent.SEND_MESSAGE

    async def handle(
        self,
        context: WebSocketContext,
        request: WebSocketRequest,
    ) -> WebSocketResponse:
        payload = SendMessageRequest.model_validate(
            request.data
        )

        response = await database_sync_to_async(
            TextMessageService.add_text_message
        )(
            chat_id=context.chat_id,
            user_id=context.user.id,
            dto=payload,
        )

        return WebSocketResponse(
            event=self.event,
            data=response.model_dump(mode="json"),
        )