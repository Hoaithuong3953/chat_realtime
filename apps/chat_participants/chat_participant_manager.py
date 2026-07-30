from __future__ import annotations
from typing import TYPE_CHECKING
from uuid import UUID
from django.db import models
from django.utils import timezone

from apps.chat_participants.enums import ParticipantRole

if TYPE_CHECKING:
    from apps.chat_participants.chat_participants_models import ChatParticipant

class ChatParticipantManager(models.Manager["ChatParticipant"]):
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

    def is_participant(self, chat_id: UUID, user_id: UUID) -> bool:
        """Check if a user is a part of chat"""
        return self.filter(
            chat_id=chat_id,
            user_id=user_id,
        ).exists()

    def get_participant(self, chat_id: UUID, user_id: UUID):
        """Get participant infomation"""
        return self.filter(
            chat_id=chat_id,
            user_id=user_id,
        ).first()
    
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
            chat_id=chat_id,
            left_at__isnull=True,
        ).count()
    
    def get_members_list(self, chat_id: UUID):
        """Retrieve all member in group"""
        return (
            self.select_related("user")
            .filter(
                chat_id=chat_id,
                left_at__isnull=True,
            )
        )
    
    def get_active_members(self, chat_id: UUID, member_ids: list[UUID]):
        """Retrieve members is active in group from list"""
        return (
            self.filter(
                chat_id=chat_id,
                user_id__in=member_ids,
                left_at__isnull=True,
            )
        )

    def leave_member(self, chat_id: UUID, member_id: UUID):
        """Update user has left the group"""
        return self.filter(
            chat_id=chat_id,
            user_id=member_id,
            left_at__isnull=True,
        ).update(left_at=timezone.now())

    def transfer_ownership(
        self,
        chat_id: UUID,
        current_owner_id: UUID,
        new_owner_id: UUID,
    ) -> None:
        """Transfer ownership to another user"""
        self.filter(
            chat_id=chat_id,
            user_id=current_owner_id,
            left_at__isnull=True,
        ).update(role=ParticipantRole.MEMBER)

        self.filter(
            chat_id=chat_id,
            user_id=new_owner_id,
            left_at__isnull=True,
        ).update(role=ParticipantRole.OWNER)

    def rejoin_members(self, chat_id, member_ids):
        """Add users who have previously left the group"""
        return self.filter(
            chat_id=chat_id,
            user_id__in=member_ids,
            left_at__isnull=False,
        ).update(
            left_at=None,
            joined_at=timezone.now(),
        )

    def get_inactive_members(self, chat_id: UUID, user_ids: list[UUID]):
        """Retrieve users who have previously left the group"""
        return self.filter(
            chat_id=chat_id,
            user_id__in=user_ids,
            left_at__isnull=False,
        )

    def get_other_participants(
        self,
        chat_ids: list[UUID],
        current_user_id: UUID,
    ):
        return (
            self.select_related("user")
            .exclude(user_id=current_user_id)
            .filter(chat_id__in=chat_ids)
        )