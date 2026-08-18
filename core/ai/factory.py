from django.conf import settings

from .protocols import AIProvider
from core.ai.providers import GeminiProvider
from shared.exceptions.ai import UnsupportedAIProviderException

def get_ai_provider() -> AIProvider:
    ai_provider = settings.AI_PROVIDER

    if ai_provider == "gemini":
        return GeminiProvider(
            api_key=settings.GEMINI_API_KEY,
            model=settings.GEMINI_MODEL,
        )

    raise UnsupportedAIProviderException(provider=ai_provider)