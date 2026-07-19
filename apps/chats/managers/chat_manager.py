from django.db import models

from apps.chats.enums import ChatType

class ChatManager(models.Manager):
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