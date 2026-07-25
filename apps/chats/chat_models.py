from django.utils import timezone
from django.db import models

from apps.chats.constants import (
    AVATAR_URL_MAX_LENGTH,
    TITLE_MAX_LENGTH,
    TYPE_MAX_LENGTH,
    PRIVATE_KEY_MAX_LENGTH,
)
from shared.base_models import BaseSoftDeleteModel
from apps.chats.enums import ChatType
from apps.chats.chat_manager import ChatManager

class Chat(BaseSoftDeleteModel):
    """Represents the chat information"""
    type = models.CharField(
        max_length=TYPE_MAX_LENGTH,
        choices=ChatType.choices,
    )
    title = models.CharField(max_length=TITLE_MAX_LENGTH, blank=True)
    avatar_url = models.URLField(max_length=AVATAR_URL_MAX_LENGTH, blank=True)
    last_activity_at = models.DateTimeField(default=timezone.now)
    private_key = models.CharField(max_length=PRIVATE_KEY_MAX_LENGTH, unique=True, null=True, blank=True)
    participants = models.ManyToManyField(
        "users.User",
        through="chat_participants.ChatParticipant",
        related_name="chats",
    )

    objects: ChatManager = ChatManager()

    class Meta:
        db_table = "chats"