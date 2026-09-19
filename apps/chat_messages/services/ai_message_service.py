from apps.chat_messages.dtos import (
    AITextMessageResponse,
    CreateAIMessageRequest,
    MessageResponse,
)
from apps.chat_messages.enums import MessageType, SenderType
from apps.chat_messages.services.message_service import MessageService

class AIMessageService:

    @staticmethod
    def create_ai_message(dto: CreateAIMessageRequest) -> AITextMessageResponse:
        ai_message = MessageService.create_message(
            chat_id=dto.chat_id,
            user_id=None,
            message_type=MessageType.TEXT,
            sender_type=SenderType.AI,
            text_content=dto.text_content,
            reply_to_message=dto.reply_to_message,
        )

        return AITextMessageResponse(
            message=MessageResponse(
                id=ai_message.id,
                chat=ai_message.chat_id,
                user=ai_message.user_id,
                message_type=ai_message.message_type,
                sender_type=ai_message.sender_type,
                text_content=ai_message.text_content,
                reply_to_message=ai_message.reply_to_message.id,
                created_at=ai_message.created_at,
            )
        )