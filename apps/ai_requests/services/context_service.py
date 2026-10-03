from collections.abc import Sequence
from uuid import UUID

from apps.ai_requests.constants import RECENT_MESSAGE_LIMIT
from apps.ai_requests.dtos import AIContextMessage
from apps.ai_requests.models import MessageChunk
from apps.chat_messages.enums import SenderType
from apps.chat_messages.models import Message

class ContextService:

    @staticmethod
    def build(
        chunks: Sequence[MessageChunk],
        recent_messages: Sequence[AIContextMessage],
        query: str,
    ) -> str:
        context_parts = []

        if chunks:
            context_parts.append("Relevant conversation history:")

            for index, chunk in enumerate(chunks, start=1):
                context_parts.append(
                    f"[Context {index}]\n{chunk.content}"
                )

        if recent_messages:
            context_parts.append("Recent conversation:")

            for message in recent_messages:
                if message.sender_type == SenderType.AI:
                    sender = "AI"
                else:
                    sender = message.full_name or "Unknown User"

                context_parts.append(
                    f"{sender}: {message.text_content}"
                )

        context_parts.append(
            f"User question:\n{query}"
        )

        return "\n\n".join(context_parts)

    @staticmethod
    def build_context_messages(
        chat_id: UUID,
        limit: int = RECENT_MESSAGE_LIMIT,
    ) -> list[AIContextMessage]:
        messages = list(
            Message.objects.get_recent_messages_for_ai_context(
                chat_id=chat_id,
                limit=limit,
            )
        )

        messages.reverse()

        return [
            AIContextMessage(
                id=message.id,
                message_type=message.message_type,
                sender_type=message.sender_type,
                full_name=(
                    message.user.full_name
                    if message.user is not None
                    else None
                ),
                text_content=message.text_content,
            )
            for message in messages
        ]