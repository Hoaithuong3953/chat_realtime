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
    
    def is_member(self, chat_id: UUID, user_id: UUID) -> bool:
        """Check if a user is a member of group"""
        return self.filter(
            chat_id=chat_id,
            user_id=user_id,
        ).exists()
    
    def is_owner(self, chat_id: UUID, user_id: UUID) -> bool:
        """Check if a user is a owner of group"""
        return self.filter(
            chat_id=chat_id,
            user_id=user_id,
            role=ChatRole.OWNER,
        ).exists()
    
    def get_owner(self, chat_id: UUID):
        """Get owner user of the group chat"""
        return self.filter(
            chat_id=chat_id,
            role=ChatRole.OWNER,
        ).select_related("user").first()
    
    def get_member_count(self, chat_id: UUID) -> int:
        """The number of members in the group"""
        return self.filter(
            chat_id=chat_id
        ).count()