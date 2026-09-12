from apps.chat_messages.dtos import AITextMessageResponse, SendAIRequestRequest, MessageResponse
from apps.chat_messages.enums import MessageType, SenderType
from apps.chat_messages.services.ai_detector import AIDetector
from apps.chat_messages.services.ai_trigger_service import AITriggerService
from apps.chat_messages.services.message_service import MessageService

class AIMessageService:

    @staticmethod
    def process_ai_request(dto: SendAIRequestRequest) -> AITextMessageResponse | None:
        user_message = dto.user_message
        text_content = user_message.text_content

        detector_result = AIDetector.detect(
            text_content=text_content,
        )

        if not detector_result.detected:
            return None

        ai_response = AITriggerService.process(
            message=user_message,
        )

        ai_message = MessageService.create_message(
            chat_id=user_message.chat,
            user_id=None,
            message_type=MessageType.TEXT,
            sender_type=SenderType.AI,
            text_content=ai_response,
            reply_to_message=user_message.id,
        )

        return AITextMessageResponse(
            message=MessageResponse(
                id=ai_message.id,
                chat=ai_message.chat_id,
                user=ai_message.user_id,
                message_type=ai_message.message_type,
                sender_type=ai_message.sender_type,
                text_content=ai_message.text_content,
                reply_to_message=ai_message.reply_to_message_id,
                created_at=ai_message.created_at,
            )
        )