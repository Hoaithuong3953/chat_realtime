from django.db import models

from config import settings
from apps.chats.constants import AVATAR_URL_MAX_LENGTH, TITLE_MAX_LENGTH, TYPE_MAX_LENGTH
from shared.base_models import BaseSoftDeleteModel
from apps.chats.enums import ChatType

class ChatModel(BaseSoftDeleteModel):
    """Represents the chat information"""
    type = models.CharField(
        max_length=TYPE_MAX_LENGTH,
        choices=ChatType.choices,
    )
    title = models.CharField(max_length=TITLE_MAX_LENGTH, blank=True, null=True)
    avatar_url = models.URLField(max_length=AVATAR_URL_MAX_LENGTH, blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="account",
    )
    last_activity_at = models.DateTimeField(auto_now_add=True)
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="ChatParticipantModel",
        related_name="chats",
    )

    class Meta:
        db_table = "chats"