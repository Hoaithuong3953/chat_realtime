from django.db import models

from apps.chats.constants import ROLE_MAX_LENGTH
from apps.chat_participants.enums import ParticipantRole
from apps.chat_participants.chat_participant_manager import ChatParticipantManager

class ChatParticipant(models.Model):
    """Represents the participants who join in a chat room"""
    chat = models.ForeignKey(
        "chats.Chat",
        on_delete=models.CASCADE,
        related_name="chat_participants",
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="chat_participants",
    )
    role = models.CharField(
        max_length=ROLE_MAX_LENGTH,
        choices=ParticipantRole.choices,
        default=ParticipantRole.MEMBER,
    )
    last_seen_message = models.ForeignKey(
        "chat_messages.Message",
        on_delete=models.SET_NULL,
        related_name="last_seen_participants",
        null=True,
        blank=True,
    )
    joined_at = models.DateTimeField(auto_now_add=True)
    left_at = models.DateTimeField(blank=True, null=True)

    objects = ChatParticipantManager()

    class Meta:
        db_table = "chat_participants"
        constraints = [
            models.UniqueConstraint(
                fields=["chat", "user"],
                name="uq_chat_participant",
            )
        ]