from uuid import UUID
from django.db import models

from apps.chats.enums import ChatRole

class ChatParticipantManager(models.Manager):
    """
    Manager for Chat Participant model

    Provides method for manager chat participant
    """
    
    def create_participants(self, chat_id: UUID, user_ids: list[UUID]):
        """Add users as participants of a chat"""
        participants = []
        for user_id in user_ids:
            participants.append(
                self.model(
                    chat_id=chat_id,
                    user_id=user_id,
                )
            )

        return self.bulk_create(participants)
    
    def create_owner_participants(self, chat_id: UUID, user_id: UUID):
        """Add a user as a participant with role OWNER"""
        return self.create(
            chat_id=chat_id,
            user_id=user_id,
            role=ChatRole.OWNER,
        )