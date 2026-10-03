from uuid import UUID

from apps.ai_requests.constants import AI_CONTEXT_SYSTEM_INSTRUCTION
from apps.ai_requests.dtos import CreateAIRequestRequest, CreateAIRequestResponse
from apps.ai_requests.models import AIRequest
from apps.ai_requests.enums import AIRequestStatus
from apps.ai_requests.services.context_service import ContextService
from apps.ai_requests.services.retrieval_service import RetrievalService
from core.ai.factory import get_ai_provider
from core.ai.dtos import AIProviderRequest
from shared.exceptions.ai import AIRequestNotFoundException

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

        if ai_request is None:
            raise AIRequestNotFoundException()

        query = ai_request.input_message.text_content

        if not query:
            raise ValueError("AI input message must contain text")

        chat_id = ai_request.input_message.chat_id

        chunks = RetrievalService.retrieve(
            chat_id=chat_id,
            query=query,
        )

        recent_messages = ContextService.build_context_messages(
            chat_id=chat_id,
        )

        context = ContextService.build(
            chunks=chunks,
            recent_messages=recent_messages,
            query=query,
        )

        provider = get_ai_provider()

        provider_request = AIProviderRequest(
            instruction=AI_CONTEXT_SYSTEM_INSTRUCTION,
            input=context,
        )

        return provider.generate(request=provider_request)