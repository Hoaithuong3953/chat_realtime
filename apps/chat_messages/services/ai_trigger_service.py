from apps.chat_messages.models import Message
from apps.ai_requests.ai_service import AIService
from apps.ai_requests.dtos import CreateAIRequestRequest

class AITriggerService:

    @staticmethod
    def process(message: Message) -> str | None:
        request = AIService.create_request(
            dto=CreateAIRequestRequest(message_id=message.id),
        )

        response = AIService.process_request(request_id=request.id)

        return response.content