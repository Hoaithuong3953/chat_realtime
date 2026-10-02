from django.conf import settings

from .protocols import AIProvider, EmbeddingProvider
from core.ai.providers import GeminiProvider, GeminiEmbeddingProvider
from shared.exceptions.ai import UnsupportedAIProviderException

def get_ai_provider() -> AIProvider:
    ai_provider = settings.AI_PROVIDER

    if ai_provider == "gemini":
        return GeminiProvider(
            api_key=settings.GEMINI_API_KEY,
            model=settings.GEMINI_MODEL,
        )

    raise UnsupportedAIProviderException(provider=ai_provider)

def get_embedding_provider() -> EmbeddingProvider:
    provider_name = settings.AI_PROVIDER

    if provider_name == "gemini":
        return GeminiEmbeddingProvider(
            api_key=settings.GEMINI_API_KEY,
            model=settings.GEMINI_EMBEDDING_MODEL,
            dimension=settings.GEMINI_EMBEDDING_DIMENSION,
        )

    raise UnsupportedAIProviderException(provider=provider_name)