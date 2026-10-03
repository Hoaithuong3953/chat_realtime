from uuid import UUID
from django.db import models
from typing import TYPE_CHECKING
from pgvector.django import CosineDistance

from apps.ai_requests.constants import RETRIEVAL_TOP_K

if TYPE_CHECKING:
    from apps.ai_requests.models import MessageChunk

class MessageChunkManager(models.Manager["MessageChunk"]):

    def create_chunks(self, chunks: list[dict]) -> None:
        """Create chunk messages"""
        self.bulk_create([
            self.model(**chunk)
            for chunk in chunks
        ])

    def search_similar(
        self,
        chat_id: UUID,
        embedding: list[float],
        limit: int = RETRIEVAL_TOP_K,
    ):
        return (
            self.filter(chat_id=chat_id)
            .annotate(
                distance=CosineDistance("embedding", embedding)
            )
            .order_by("distance")[:limit]
        )