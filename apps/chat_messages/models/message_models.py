from django.db import models

from apps.chat_messages.constants import TYPE_MAX_LENGTH, TEXT_CONTENT_MAX_LENGTH, MESSAGE_STATUS_MAX_LENGTH
from apps.chat_messages.enums import MessageType, MessageStatus, SenderType
from shared.base_models import BaseSoftDeleteModel
from apps.chat_messages.managers import MessageManager

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
    sender_type = models.CharField(
        max_length=TYPE_MAX_LENGTH,
        choices=SenderType.choices,
        default=SenderType.USER,
    )
    text_content = models.TextField(max_length=TEXT_CONTENT_MAX_LENGTH, null=True, blank=True)
    reply_to_message = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        related_name="replies",
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=MESSAGE_STATUS_MAX_LENGTH,
        choices=MessageStatus.choices,
        default=MessageStatus.ACTIVE,
    )
    recalled_at = models.DateTimeField(null=True, blank=True)

    objects: MessageManager = MessageManager()

    class Meta:
        db_table = "messages"
        indexes = [
            models.Index(
                fields=["chat", "-created_at", "-id"],
                name="idx_msg_chat_created_id",
            ),
        ]