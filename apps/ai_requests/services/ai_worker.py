from uuid import UUID
from django.db import transaction
import time

from .ai_service import AIService
from apps.ai_requests.enums import AIRequestStatus
from apps.ai_requests.models import AIRequest
from apps.chat_messages.services.ai_message_service import AIMessageService
from apps.chat_messages.dtos import CreateAIMessageRequest
from apps.chat_messages.websocket.broadcaster import MessageBroadcaster
from shared.logger import logging

logger = logging.getLogger(__name__)
class AIWorker:

    @staticmethod
    def process(request_id: UUID) -> None:
        ai_request = AIRequest.objects.get_by_id(request_id=request_id)

        if ai_request is None:
            return

        if not AIRequest.objects.claim_request(request_id=request_id):
            return

        time.sleep(15)

        try:
            response = AIService.process_request(request_id=request_id)

            with transaction.atomic():
                dto = CreateAIMessageRequest(
                    chat_id=ai_request.input_message.chat_id,
                    reply_to_message=ai_request.input_message.id,
                    text_content=response.content,
                )
                ai_response = AIMessageService.create_ai_message(dto=dto)

                AIRequest.objects.update_request(
                    request_id=request_id,
                    status=AIRequestStatus.COMPLETED,
                    output_message_id=ai_response.message.id,
                )

        except Exception as e:
            AIRequest.objects.update_request(
                request_id=request_id,
                status=AIRequestStatus.FAILED,
                error_message=str(e),
            )
            return

        try:
            MessageBroadcaster.broadcast_sync(
                chat_id=ai_request.input_message.chat_id,
                message=ai_response.model_dump(mode="json"),
            )
        except Exception:
            logger.exception(f"Failed to broadcast AI response for request {request_id}")