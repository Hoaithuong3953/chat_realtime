from uuid import UUID

from apps.chat_messages.dtos import (
    SendTextMessageRequest,
    SendTextMessageResponse,
    MessageResponse,
)
from apps.chat_messages.enums import MessageType, SenderType
from .message_service import MessageService
from .ai_trigger_service import AITriggerService
from .ai_detector import AIDetector

class TextMessageService:

        @staticmethod
        def add_text_message(chat_id: UUID, user_id: UUID, dto: SendTextMessageRequest) -> SendTextMessageResponse:
            """
            Add a text message in to the chat
            """
            detection = AIDetector.detect(dto.text_content)

            if detection.detected:
                text_content = detection.input
            else:
                text_content=dto.text_content

            user_message = MessageService.create_message(
                chat_id=chat_id,
                user_id=user_id,
                message_type=MessageType.TEXT,
                sender_type=SenderType.USER,
                text_content=text_content,
                reply_to_message=dto.reply_to_message,
            )

            user_message_response =  MessageResponse(
                id=user_message.id,
                chat=chat_id,
                user=user_id,
                message_type=user_message.message_type,
                sender_type=user_message.sender_type,
                text_content=user_message.text_content,
                reply_to_message=user_message.reply_to_message_id,
                created_at=user_message.created_at,
            )

            ai_message_response = None

            if detection.detected:
                ai_response = AITriggerService.process(user_message)

                ai_message = MessageService.create_message(
                    chat_id=chat_id,
                    user_id=None,
                    message_type=MessageType.TEXT,
                    sender_type=SenderType.AI,
                    text_content=ai_response,
                    reply_to_message=user_message.id,
                )

                ai_message_response = MessageResponse(
                    id=ai_message.id,
                    chat=chat_id,
                    user=None,
                    message_type=ai_message.message_type,
                    sender_type=ai_message.sender_type,
                    text_content=ai_message.text_content,
                    reply_to_message=ai_message.reply_to_message_id,
                    created_at=ai_message.created_at,
                )

            return SendTextMessageResponse(
                user_message=user_message_response,
                ai_message=ai_message_response,
            )