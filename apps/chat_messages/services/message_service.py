from datetime import timedelta
from uuid import UUID
from django.db import transaction
from django.utils import timezone

from apps.chat_messages.dtos import RecallMessageResponse
from apps.chat_messages.enums import MessageStatus, MessageType, SenderType
from apps.chat_messages.models.file_message_model import FileMessage
from apps.file_assets.models import FileAsset
from shared.exceptions.chat.common import ChatAccessDeniedException, ChatNotFoundException
from shared.exceptions.chat.message import (
    MessageAlreadyRecalledException,
    MessageNotFoundException,
    MessageRecallTimeExpiredException,
    NoPermissionToRecallException,
    ReplyMessageNotFoundException,
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

        if message.message_type == MessageType.FILE:
            file_id = FileMessage.objects.get_file_id_by_message_id(message_id)

        with transaction.atomic():
            message = Message.objects.recall(message=message)

            if file_id:
                FileAsset.objects.delete_file(file_id=file_id)

        return RecallMessageResponse.model_validate(message)

    @staticmethod
    def _can_recall_message(message: Message) -> bool:
        recall_deadline = message.created_at + timedelta(minutes=5)
        return timezone.now() <= recall_deadline

    @staticmethod
    def create_message(
        chat_id: UUID,
        user_id: UUID,
        message_type: MessageType,
        sender_type: SenderType,
        text_content: str | None,
        reply_to_message: UUID | None,
    ) -> Message:
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
        if reply_to_message is not None:
            reply_to_message = Message.objects.get_by_chat_and_id(reply_to_message, chat_id)

            if reply_to_message is None:
                raise ReplyMessageNotFoundException()

        with transaction.atomic():
            message = Message.objects.create_message(
                chat_id=chat_id,
                user_id=user_id,
                message_type=message_type,
                sender_type=sender_type,
                text_content=text_content,
                reply_to=reply_to_message,
            )
            Chat.objects.update_last_activity(chat_id=chat.id)
            Chat.objects.update_last_message(chat_id=chat.id, message_id=message.id)

        return message