from django.db import models

from apps.chat_messages.constants import TYPE_MAX_LENGTH, TEXT_CONTENT_MAX_LENGTH
from apps.chat_messages.enums import MessageType
from shared.base_models import BaseSoftDeleteModel
from apps.chat_messages.message_manager import MessageManager

class Message(BaseSoftDeleteModel):
    """Represents the content of user message"""
    chat = models.ForeignKey(
        "chats.Chat",
        on_delete=models.CASCADE,
        related_name="messages"
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="messages"
    )
    message_type = models.CharField(
        max_length=TYPE_MAX_LENGTH,
        choices=MessageType.choices,
        default=MessageType.TEXT,
    )
    text_content = models.TextField(max_length=TEXT_CONTENT_MAX_LENGTH, null=True, blank=True)
    reply_to_message = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        related_name="replies",
        null=True,
        blank=True,
    )
    revoked_at = models.DateTimeField(null=True, blank=True)

    objects: MessageManager = MessageManager()

    class Meta:
        db_table = "messages"