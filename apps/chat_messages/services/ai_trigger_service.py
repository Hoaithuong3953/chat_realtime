from uuid import UUID

from apps.ai_requests.queue import AIRequestQueue
from apps.ai_requests.services.ai_service import AIService
from apps.ai_requests.dtos import CreateAIRequestRequest
from apps.chat_messages.models import Message
from apps.chat_messages.services.ai_detector import AIDetector
from shared.logger import logging

logger = logging.getLogger(__name__)
class AITriggerService:

    @staticmethod
    def process(message_id: UUID) -> None:
        message = Message.objects.get_by_id(message_id=message_id)

        if message is None:
            logger.warning(f"Message not found: {message_id}")
            return

        result = AIDetector.detect(
            text_content=message.text_content,
        )

        if not result.detected:
            return

        request = AIService.create_request(
            dto=CreateAIRequestRequest(message_id=message_id),
        )

        logger.info(f"AI request queued: request={request.id}, message={message.id}, input={result.input}")

        AIRequestQueue.enqueue(
            request_id=request.id,
            input=result.input,
        )