from django.db import models
from pgvector.django import VectorField

from shared.base_models import BaseModel
from apps.ai_requests.constants import EMBEDDING_DIMENSION
from apps.ai_requests.managers import MessageChunkManager

class MessageChunk(BaseModel):
    chat = models.ForeignKey(
        "chats.Chat",
        on_delete=models.CASCADE,
        related_name="message_chunks",
    )
    start_message = models.ForeignKey(
        "chat_messages.Message",
        on_delete=models.SET_NULL,
        null=True,
        related_name="+",
    )
    end_message = models.ForeignKey(
        "chat_messages.Message",
        on_delete=models.SET_NULL,
        null=True,
        related_name="+",
    )
    content = models.TextField()
    embedding = VectorField(dimensions=EMBEDDING_DIMENSION)

    objects: MessageChunkManager = MessageChunkManager()

    class Meta:
        db_table = "message_chunks"
        indexes = [
            models.Index(
                fields=["chat", "created_at"],
                name="idx_chunk_chat_created",
            ),
        ]