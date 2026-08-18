from typing import Protocol

from .dtos import AIRequest, AIResponse

class AIProvider(Protocol):
    def generate(self, request: AIRequest) -> AIResponse:
        """Generate a response from the AI provider"""
        ...