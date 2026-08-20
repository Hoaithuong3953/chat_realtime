from typing import Protocol

from .dtos import AIProviderRequest, AIProviderResponse

class AIProvider(Protocol):
    def generate(self, request: AIProviderRequest) -> AIProviderResponse:
        """Generate a response from the AI provider"""
        ...