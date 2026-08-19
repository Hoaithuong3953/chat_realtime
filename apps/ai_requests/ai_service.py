from apps.ai_requests.dtos import CreateAIRequestRequest, CreateAIRequestResponse
from apps.ai_requests.models import AIRequest
from apps.ai_requests.enums import AIRequestStatus

class AIService:

    @staticmethod
    def create_request(dto: CreateAIRequestRequest, model: str) -> CreateAIRequestResponse:
        """
        Create a request to send to the AI service
        """
        return AIRequest.objects.create_request(
            input_message_id=dto.message_id,
            status=AIRequestStatus.QUEUED,
            model=model,
        )