from collections.abc import Sequence

from apps.ai_requests.constants import CHUNK_OVERLAP, CHUNK_SIZE
from apps.ai_requests.dtos import AIContextMessage
from apps.chat_messages.enums import MessageType, SenderType

def chunk_messages(
    messages: Sequence[AIContextMessage],
    chunk_size: int = CHUNK_SIZE,
    overlap: int = CHUNK_OVERLAP,
) -> list[list[AIContextMessage]]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")

    if overlap < 0:
        raise ValueError("overlap must not be negative")

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    if not messages:
        return []

    chunks = []
    start = 0
    step = chunk_size - overlap

    while start < len(messages):
        chunk = list(messages[start:start + chunk_size])

        if not chunk:
            break

        chunks.append(chunk)

        if start + chunk_size >= len(messages):
            break

        start += step

    return chunks

def format_chunk(messages: Sequence[AIContextMessage]) -> str:
    parts = []

    for message in messages:
        if message.message_type != MessageType.TEXT:
            continue

        if message.sender_type == SenderType.AI:
            sender = "AI"
        else:
            sender = message.full_name or "Unknown User"

        parts.append(
            f"[{message.created_at.isoformat()}] "
            f"{sender}: {message.text_content}"
        )

    return "\n".join(parts)