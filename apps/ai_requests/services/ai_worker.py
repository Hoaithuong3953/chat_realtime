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
    def process(request_id: UUID, input: str) -> None:
        ai_request = AIRequest.objects.get_by_id(request_id=request_id)

        if ai_request is None:
            logger.warning(f"AI request not found: {request_id}")
            return

        if ai_request.status in (AIRequestStatus.COMPLETED, AIRequestStatus.COMPLETED):
            return

        if ai_request.status == AIRequestStatus.QUEUED:
            claimed = AIRequest.objects.claim_request(request_id=request_id)

            if not claimed:
                return

            ai_request.refresh_from_db()

        if ai_request.status != AIRequestStatus.PROCESSING:
            return

        AIRequest.objects.increment_attempt_count(request_id=request_id)

        response = AIService.process_request(request_id=request_id)
        
        with transaction.atomic():
            ai_request = AIRequest.objects.get_for_update(request_id=request_id)

            if ai_request.status == AIRequestStatus.COMPLETED:
                return

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
                error_message=None,
            )
        
        try:
            MessageBroadcaster.broadcast_sync(
                chat_id=ai_request.input_message.chat_id,
                message=ai_response.model_dump(mode="json"),
            )
        except Exception:
            logger.exception(f"Failed to broadcast AI response for request {request_id}")

    @staticmethod
    def mark_failed(request_id: UUID, error_message: str) -> None:
        AIRequest.objects.update_request(
            request_id=request_id,
            status=AIRequestStatus.FAILED,
            error_message=error_message,
        )