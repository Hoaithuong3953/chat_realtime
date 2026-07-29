from datetime import timedelta
from uuid import UUID
from django.db import transaction
from django.utils import timezone

from apps.chat_messages.dtos import (
    SendMessageRequest,
    SendMessageResponse,
    RecallMessageResponse,
)
from apps.chats.chat_models import Chat
from apps.chat_participants.chat_participants_models import ChatParticipant
from apps.chat_messages.models import Message
from apps.chat_messages.exceptions import (
    ChatAccessDeniedException,
    ChatNotFoundException,
    ReplyMessageNotFoundException,
    MessageNotFoundException,
    MessageAlreadyRecalledException,
    MessageRecallTimeExpiredException,
    NoPermissionToRecallException,
)
from apps.chat_messages.enums import MessageStatus

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
                message = Message.objects.create_text_message(
                    chat_id=chat.id,
                    sender_id=user_id,
                    content=dto.text_content,
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

        @staticmethod
        def recall_message(chat_id: UUID, user_id: UUID, message_id: UUID) -> RecallMessageResponse:
            """
            Recall a message in a chat
            
            Raises:
                ChatNotFoundException: if chat not found
                MessageNotFoundException: if the message cannot found
                ChatAccessDeniedException: if the user is not part of the chat
                NoPermissionToRecallException: if the user is not the sender
                MessageAlreadyRecalledException: if the message was recalled
                MessageRecallTimeExpiredException: if the time to recall message is expired
            """
            chat = Chat.objects.get_chat_by_id(chat_id=chat_id)

            # Check if chat cannot found
            if chat is None:
                raise ChatNotFoundException()

            message = Message.objects.get_by_chat_and_id(
                message_id=message_id,
                chat_id=chat_id,
            )

            # Check if message cannot found
            if message is None:
                raise MessageNotFoundException()

            # Check if the user is not a participant of the chat
            is_participant = ChatParticipant.objects.is_participant(
                chat_id=chat_id,
                user_id=user_id
            )
            if not is_participant:
                raise ChatAccessDeniedException()

            # Check if the user is not the sender
            if message.user_id != user_id:
                raise NoPermissionToRecallException()

            # Check if the message was recalled
            if message.status == MessageStatus.RECALLED:
                raise MessageAlreadyRecalledException()

            # Check if the time to recall message is expired
            if not TextMessageService._can_recall_message(message):
                raise MessageRecallTimeExpiredException()

            with transaction.atomic():
                message = Message.objects.recall(message=message)

            return RecallMessageResponse.model_validate(message)

        @staticmethod
        def _can_recall_message(message) -> bool:
            recall_deadline = message.created_at + timedelta(minutes=5)
            return timezone.now() <= recall_deadline