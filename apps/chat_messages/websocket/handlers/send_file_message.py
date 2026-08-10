from channels.db import database_sync_to_async

from core.websocket.context import WebSocketContext
from core.websocket.base_handler import WebSocketHandler
from core.websocket.base_schema import WebSocketRequest, WebSocketResponse

from apps.chat_messages.services import FileMessageService
from apps.chat_messages.dtos import SendFileMessageRequest
from apps.chat_messages.websocket.events import ChatEvent

class SendFileHanlder(WebSocketHandler):
    event = ChatEvent.SEND_FILE_MESSAGE

    async def handle(self, context: WebSocketContext, request: WebSocketRequest) -> WebSocketResponse:
        dto = SendFileMessageRequest.model_validate(
            request.data
        )
        response = await database_sync_to_async(
            FileMessageService.add_file_message
        )(
            chat_id=context.chat_id,
            user_id=context.user.id,
            dto=dto,
        )

        return WebSocketResponse(
            event=self.event,
            data=response.model_dump(mode="json"),
        )