from uuid import UUID

from apps.chat_messages.dtos import (
    SendMessageRequest,
    SendMessageResponse,
)
from apps.chat_messages.enums import MessageType
from .message_service import MessageService

class TextMessageService:

        @staticmethod
        def add_text_message(chat_id: UUID, user_id: UUID, dto: SendMessageRequest) -> SendMessageResponse:
            """
            Add a text message in to the chat
            """
            message = MessageService.create_message(
                chat_id=chat_id,
                user_id=user_id,
                message_type=MessageType.TEXT,
                text_content=dto.text_content,
                reply_to_message=dto.reply_to_message,
            )

            return SendMessageResponse(
                id=message.id,
                chat=chat_id,
                user=user_id,
                message_type=message.message_type,
                text_content=message.text_content,
                reply_to_message=message.reply_to_message_id,
                created_at=message.created_at,
            )