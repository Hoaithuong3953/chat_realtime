from core.ai.factory import get_embedding_provider
from core.ai.dtos import EmbeddingProviderRequest, EmbeddingProviderResponse

class EmbeddingService:

    @staticmethod
    def embed(text: str) -> EmbeddingProviderResponse:
        provider = get_embedding_provider()

        request = EmbeddingProviderRequest(input=text)

        return provider.embed(request=request)