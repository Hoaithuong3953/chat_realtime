from __future__ import annotations
from typing import TYPE_CHECKING
from uuid import UUID
from django.db import models
from django.db.models import Q
from django.utils import timezone

from apps.chat_messages.enums import MessageType, MessageStatus

if TYPE_CHECKING:
    from apps.chat_messages.models import Message

class MessageManager(models.Manager["Message"]):
    """
    Manager for Chat Message model

    Provides method for manager chat message
    """
    def create_text_message(
        self,
        chat_id: UUID,
        sender_id: UUID,
        content: str,
        reply_to: UUID | None,
    ):
        """Add message to chat"""
        return self.create(
            chat_id=chat_id,
            user_id=sender_id,
            message_type=MessageType.TEXT,
            text_content=content,
            reply_to_message_id=reply_to,
        )

    def get_by_chat_and_id(self, message_id: UUID, chat_id: UUID):
        """Get a message by chat id and message id"""
        return self.filter(
            chat_id=chat_id,
            id=message_id,
        ).first()

    def get_chat_history(
        self,
        chat_id: UUID,
        cursor: str | None,
        limit: int,
    ):
        """Get list messages from a chat"""
        qs = (
            self.filter(chat_id=chat_id)
            .order_by("-created_at", "-id")
        )

        if cursor:
            qs = qs.filter(
                Q(created_at__lt=cursor.created_at) | 
                (Q(created_at=cursor.created_at)&Q(id__lt=cursor.message_id))
            )

        return list(qs[:limit])

    def recall(self, message: Message):
        message.status = MessageStatus.RECALLED
        message.recalled_at = timezone.now()
        message.save(update_fields=["status", "recalled_at"])
        return message