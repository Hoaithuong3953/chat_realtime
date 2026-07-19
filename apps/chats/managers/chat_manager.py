from uuid import UUID

from django.db import models

from apps.chats.enums import ChatType

class ChatManager(models.Manager):
    """
    Manager for Chat model

    Provides method for manager chat
    """
    def get_private_chat(self, user1_id: UUID, user2_id: UUID):
        """Retrieve existing private chat"""
        return (
            self.filter(type=ChatType.PRIVATE)
            .filter(participants__id=user1_id)
            .filter(participants__id=user2_id)
            .first()
        )
    
    def create_private_chat(self):
        """Create a new private chat"""
        return self.create(
            type=ChatType.PRIVATE,
        )