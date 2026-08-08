from channels.db import database_sync_to_async

from core.websocket.context import WebSocketContext
from core.websocket.base_handler import WebSocketHandler
from core.websocket.base_schema import WebSocketRequest, WebSocketResponse

from apps.chat_messages.services import DocumentMessageService
from apps.chat_messages.dtos import SendDocumentMessageRequest
from apps.chat_messages.websocket.events import ChatEvent

class SendDocumentHanlder(WebSocketHandler):
    event = ChatEvent.SEND_DOCUMENT_MESSAGE

    async def handle(self, context: WebSocketContext, request: WebSocketRequest) -> WebSocketResponse:
        dto = SendDocumentMessageRequest.model_validate(
            request.data
        )
        response = await database_sync_to_async(
            DocumentMessageService.add_document_mesage
        )(
            chat_id=context.chat_id,
            user_id=context.user.id,
            dto=dto,
        )

        return WebSocketResponse(
            event=self.event,
            data=response.model_dump(mode="json"),
        )