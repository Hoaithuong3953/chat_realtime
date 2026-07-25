from __future__ import annotations
from typing import TYPE_CHECKING
from uuid import UUID
from django.db import models

from apps.chat_messages.enums import MessageType

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