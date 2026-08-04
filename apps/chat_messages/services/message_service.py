from datetime import timedelta
from uuid import UUID

from django.db import transaction
from django.utils import timezone

from apps.chat_messages.dtos import RecallMessageResponse
from apps.chat_messages.enums import MessageStatus
from apps.chat_messages.exceptions import (
    ChatAccessDeniedException,
    ChatNotFoundException,
    MessageAlreadyRecalledException,
    MessageNotFoundException,
    MessageRecallTimeExpiredException,
    NoPermissionToRecallException,
)
from apps.chat_messages.models import Message
from apps.chat_participants.models import ChatParticipant
from apps.chats.models import Chat

class MessageService:
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
        if not MessageService._can_recall_message(message):
            raise MessageRecallTimeExpiredException()

        with transaction.atomic():
            message = Message.objects.recall(message=message)

        return RecallMessageResponse.model_validate(message)

    @staticmethod
    def _can_recall_message(message: Message) -> bool:
        recall_deadline = message.created_at + timedelta(minutes=5)
        return timezone.now() <= recall_deadline