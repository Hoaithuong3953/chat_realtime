from google import genai
from google.genai import types

from core.ai.dtos import AIProviderResponse, AIProviderRequest

class GeminiProvider:
    def __init__(self, api_key: str, model: str) -> None:
        self.model = model
        self.client = genai.Client(
            api_key=api_key,
            http_options=types.HttpOptions(
                retry_options=types.HttpRetryOptions(attempts=1),
                timeout=90_000,
            )
        )

    def generate(self, request: AIProviderRequest) -> AIProviderResponse:
        response = self.client.models.generate_content(
            model=self.model,
            contents=request.input,
            config={
                "system_instruction": request.instruction,
            },
        )

        return AIProviderResponse(
            content=response.text,
            model=self.model,
        )