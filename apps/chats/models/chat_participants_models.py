from django.db import models

from apps.chats.constants import ROLE_MAX_LENGTH
from apps.chats.enums import ChatRole

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
        choices=ChatRole.choices,
        default=ChatRole.MEMBER,
    )
    joined_at = models.DateTimeField(auto_now_add=True)
    left_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "chat_participants"
        constraints = [
            models.UniqueConstraint(
                fields=["chat", "user"],
                name="uq_chat_participant",
            )
        ]