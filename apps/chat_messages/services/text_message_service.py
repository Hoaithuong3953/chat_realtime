from uuid import UUID
from django.db import transaction

from apps.chat_messages.dtos import (
    SendMessageRequest,
    SendMessageResponse,
)
from apps.chats.models import Chat
from apps.chat_participants.models import ChatParticipant
from apps.chat_messages.models import Message
from apps.chat_messages.exceptions import (
    ChatAccessDeniedException,
    ChatNotFoundException,
    ReplyMessageNotFoundException,
)
from apps.chat_messages.enums import MessageType

class TextMessageService:

        @staticmethod
        def add_text_message(chat_id: UUID, user_id: UUID, dto: SendMessageRequest) -> SendMessageResponse:
            """
            Add a message in to the chat

            Raises:
                ChatAccessDeniedException: if the user is not part of the chat
                ChatNotFoundException: if chat not found
                ReplyMessageNotFoundException: if cannot find the replied messages
            """
            # Check if is the chat exist
            chat = Chat.objects.get_chat_by_id(chat_id)
            if not chat:
                raise ChatNotFoundException()

            # Check if the user is a part of the chat
            is_participant = ChatParticipant.objects.is_participant(chat_id, user_id)
            if not is_participant:
                raise ChatAccessDeniedException()

            # Check if the reply message is exist
            if dto.reply_to_message is not None:
                reply_message = Message.objects.get_by_chat_and_id(dto.reply_to_message, chat_id)

                if reply_message is None:
                    raise ReplyMessageNotFoundException()

            with transaction.atomic():
                message = Message.objects.create_message(
                    chat_id=chat.id,
                    user_id=user_id,
                    message_type=MessageType.TEXT,
                    text_content=dto.text_content,
                    reply_to=dto.reply_to_message,
                )
                Chat.objects.update_last_activity(chat_id=chat.id)
                Chat.objects.update_last_message(chat_id=chat.id, message_id=message.id)

            return SendMessageResponse(
                id=message.id,
                chat=chat_id,
                user=user_id,
                message_type=message.message_type,
                text_content=message.text_content,
                reply_to_message=message.reply_to_message_id,
                created_at=message.created_at,
            )