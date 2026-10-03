from uuid import UUID

from apps.ai_requests.constants import RETRIEVAL_TOP_K
from apps.ai_requests.models import MessageChunk
from apps.ai_requests.services.embedding_service import EmbeddingService

class RetrievalService:

    @staticmethod
    def retrieve(chat_id: UUID, query: str):
        embedding_response = EmbeddingService.embed(query)

        return MessageChunk.objects.search_similar(
            chat_id=chat_id,
            embedding=embedding_response.embedding,
            limit=RETRIEVAL_TOP_K,
        )