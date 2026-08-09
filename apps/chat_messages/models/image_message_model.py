import uuid
from django.db import models

from apps.chat_messages.managers import ImageMessageManager

class ImageMessage(models.Model):
    """Link a message with attached images"""
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    message = models.ForeignKey(
        "chat_messages.Message",
        on_delete=models.CASCADE,
        related_name="image_message",
    )
    asset = models.ForeignKey(
        "file_assets.FileAsset",
        on_delete=models.CASCADE,
        related_name="image_message",
    )
    position = models.PositiveBigIntegerField()
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()

    objects: ImageMessageManager = ImageMessageManager()

    class Meta:
        db_table = "image_messages"
        constraints = [
            models.UniqueConstraint(
                fields=["message", "position"],
                name="uq_image_message_position",
            ),
        ]
        ordering = ["position"]
        