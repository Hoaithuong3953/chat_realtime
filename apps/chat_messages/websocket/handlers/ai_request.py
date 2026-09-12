from channels.db import database_sync_to_async

from apps.chat_messages.dtos.message_dto import MessageResponse
from apps.chat_messages.websocket.events import ChatEvent
from apps.chat_messages.dtos import SendAIRequestRequest, AITextMessageResponse
from apps.chat_messages.services import AIMessageService

from core.websocket.base_handler import WebSocketHandler

class AIRequestHandler(WebSocketHandler):
    event = ChatEvent.AI_REQUEST

    async def handle(
        self,
        user_message: MessageResponse,
    ) -> AITextMessageResponse | None:
        dto = SendAIRequestRequest(user_message=user_message)

        return await database_sync_to_async(
            AIMessageService.process_ai_request
        )(dto=dto)