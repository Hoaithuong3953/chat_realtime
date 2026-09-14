from uuid import UUID

from apps.ai_requests.queue import AIRequestQueue
from apps.ai_requests.services import AIService
from apps.ai_requests.dtos import CreateAIRequestRequest

class AITriggerService:

    @staticmethod
    def process(message_id: UUID) -> None:
        request = AIService.create_request(
            dto=CreateAIRequestRequest(message_id=message_id),
        )

        AIRequestQueue.enqueue(request_id=request.id)