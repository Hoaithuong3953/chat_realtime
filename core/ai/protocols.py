from typing import Protocol

from .dtos import AIProviderRequest, AIProviderResponse

class AIProvider(Protocol):
    def generate(self, request: AIProviderRequest) -> AIProviderResponse:
        """Generate a response from the AI provider"""
        ...

class EmbeddingProvider(Protocol):
    def embed(self, input: str) -> list[float]:
        """Generate a vector embedding for the given input text"""
        ...