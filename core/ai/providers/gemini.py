from google import genai

from core.ai.dtos import AIRequest, AIResponse
from shared.exceptions.ai import AIProviderException

class GeminiProvider:
    def __init__(self, api_key: str, model: str) -> None:
        self.model = model
        self.client = genai.Client(api_key=api_key)

    def generate(self, request: AIRequest) -> AIResponse:
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=request.input,
                config={
                    "system_instruction": request.instruction,
                },
            )

            return AIResponse(
                content=response.text,
                model=self.model,
            )

        except Exception as exc:
            raise AIProviderException() from exc