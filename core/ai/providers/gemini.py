from google import genai
from google.genai import types

from core.ai.dtos import (
    AIProviderRequest,
    AIProviderResponse,
    EmbeddingProviderRequest,
    EmbeddingProviderResponse,
)

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

class GeminiEmbeddingProvider:
    def __init__(self, api_key: str, model: str, dimension: int) -> None:
        self.model = model
        self.dimension = dimension
        self.client = genai.Client(
            api_key=api_key,
            http_options=types.HttpOptions(
                retry_options=types.HttpRetryOptions(attempts=1),
                timeout=90_000,
            )
        )

    def embed(self, request: EmbeddingProviderRequest) -> EmbeddingProviderResponse:
        response = self.client.models.embed_content(
            model=self.model,
            config=types.EmbedContentConfig(
                output_dimensionality=self.dimension,
            ),
            contents=request.input,
        )

        return EmbeddingProviderResponse(
            embedding=response.embeddings[0].values,
            model=self.model,
        )