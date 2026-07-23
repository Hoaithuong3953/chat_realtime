from uuid import UUID
from django.db import models
from django.utils import timezone

from apps.chat_participants.enums import ParticipantRole

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
            role=ParticipantRole.OWNER,
        )
    
    def is_member(self, chat_id: UUID, user_id: UUID) -> bool:
        """Check if a user is a member of group"""
        return self.filter(
            chat_id=chat_id,
            user_id=user_id,
            left_at__isnull=True,
        ).exists()
    
    def is_owner(self, chat_id: UUID, user_id: UUID) -> bool:
        """Check if a user is a owner of group"""
        return self.filter(
            chat_id=chat_id,
            user_id=user_id,
            role=ParticipantRole.OWNER,
            left_at__isnull=True,
        ).exists()
    
    def get_owner(self, chat_id: UUID):
        """Get owner user of the group chat"""
        return self.filter(
            chat_id=chat_id,
            role=ParticipantRole.OWNER,
            left_at__isnull=True,
        ).select_related("user").first()
    
    def get_member_count(self, chat_id: UUID) -> int:
        """The number of members in the group"""
        return self.filter(
            chat_id=chat_id
        ).count()
    
    def get_members_list(self, chat_id: UUID):
        return (
            self.select_related("user")
            .filter(
                chat_id=chat_id,
                left_at__isnull=True,
            )
        )
    
    def get_existing_members(self, chat_id: UUID, member_ids: list[UUID]):
        return (
            self.filter(
                chat_id=chat_id,
                user_id__in=member_ids,
                left_at__isnull=True,
            )
        )

    def delete_member(self, chat_id: UUID, member_id: UUID):
        return self.filter(
            chat_id=chat_id,
            user_id=member_id,
            left_at__isnull=True,
        ).update(left_at=timezone.now())