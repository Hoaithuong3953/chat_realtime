from collections.abc import Sequence
from uuid import UUID

from apps.ai_requests.dtos import AIContextMessage
from apps.ai_requests.models import MessageChunk
from apps.ai_requests.services.chunk_service import chunk_messages, format_chunk
from apps.ai_requests.services.embedding_service import EmbeddingService
from apps.chat_messages.models import Message

class MessageChunkService:

    @staticmethod
    def create_chunks(
        chat_id: UUID,
        messages: Sequence[AIContextMessage],
    ) -> None:
        chunks = chunk_messages(messages)

        chunk_data = []

        for chunk in chunks:
            content = format_chunk(chunk)

            if not content:
                continue

            embedding_response = EmbeddingService.embed(content)

            chunk_data.append({
                "chat_id": chat_id,
                "start_message_id": chunk[0].id,
                "end_message_id": chunk[-1].id,
                "content": content,
                "embedding": embedding_response.embedding,
            })

        if chunk_data:
            MessageChunk.objects.create_chunks(chunk_data)