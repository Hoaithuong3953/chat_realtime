from channels.db import database_sync_to_async

from core.websocket.base_schema import WebSocketRequest, WebSocketResponse
from core.websocket.context import WebSocketContext
from core.websocket.base_handler import WebSocketHandler
from apps.chat_messages.websocket.events import ChatEvent
from apps.chat_messages.dtos import RecallMessageRequest
from apps.chat_messages.services import MessageService

class RecallMessageHandler(WebSocketHandler):
    event = ChatEvent.RECALL_MESSAGE

    async def handle(
        self,
        context: WebSocketContext,
        request: WebSocketRequest,
    ) -> WebSocketResponse:
        payload = RecallMessageRequest.model_validate(
            request.data,
        )

        response = await database_sync_to_async(
            MessageService.recall_message
        )(
            chat_id=context.chat_id,
            user_id=context.user.id,
            message_id=payload.message_id,
        )

        return WebSocketResponse(
            event=self.event,
            data=response.model_dump(mode="json")
        )