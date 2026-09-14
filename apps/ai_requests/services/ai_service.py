from uuid import UUID

from apps.ai_requests.dtos import CreateAIRequestRequest, CreateAIRequestResponse
from apps.ai_requests.models import AIRequest
from apps.ai_requests.enums import AIRequestStatus
from core.ai.factory import get_ai_provider
from core.ai.dtos import AIProviderRequest

class AIService:

    @staticmethod
    def create_request(dto: CreateAIRequestRequest) -> CreateAIRequestResponse:
        """
        Create a request to send to the AI service
        """
        provider = get_ai_provider()

        return AIRequest.objects.create_request(
            input_message_id=dto.message_id,
            status=AIRequestStatus.QUEUED,
            model=provider.model,
        )

    @staticmethod
    def process_request(request_id: UUID):
        """
        Process the request sent to the AI service
        """
        ai_request = AIRequest.objects.get_by_id(request_id=request_id)

        provider = get_ai_provider()
        provider_request = AIProviderRequest(
            input=ai_request.input_message.text_content,
        )

        return provider.generate(request=provider_request)