from __future__ import annotations
from uuid import UUID
from django.db import models
from django.utils import timezone
from typing import TYPE_CHECKING

from apps.chats.enums import ChatType

if TYPE_CHECKING:
    from apps.chats.chat_models import Chat

class ChatManager(models.Manager["Chat"]):
    """
    Manager for Chat model

    Provides method for manager chat
    """
    def get_private_chat(self, private_key: str):
        """Retrieve existing private chat"""
        return (
            self.filter(
                type=ChatType.PRIVATE,
                private_key=private_key,
            )
            .first()
        )
    
    def create_private_chat(self, private_key: str):
        """Create a new private chat"""
        return self.create(
            type=ChatType.PRIVATE,
            private_key=private_key,
        )
    
    def create_group_chat(self, title: str):
        """Create a new group chat"""
        return self.create(
            type=ChatType.GROUP,
            title=title,
        )
    
    def get_chat_by_id(self, chat_id: UUID):
        """Retrieve existing a chat"""
        return self.filter(
            id=chat_id,
        ).first()
    
    def update_group_chat_info(self, chat, **fields):
        """Update group chat information"""
        for field, value in fields.items():
            setattr(chat, field, value)

        chat.save(update_fields=[*fields.keys(), "updated_at"])
        return chat

    def update_last_activity(self, chat_id: UUID) -> None:
        """Update the chat's last activity timestamp"""
        self.filter(id=chat_id).update(
            last_activity_at=timezone.now()
        )