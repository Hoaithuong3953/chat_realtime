from django.db import models

from apps.chat_messages.managers import FileMessageManager

class FileMessage(models.Model):
    """Link a message with a file attachment"""
    message = models.OneToOneField(
        "chat_messages.Message",
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="file_message",
    )
    file_asset = models.ForeignKey(
        "file_assets.FileAsset",
        on_delete=models.CASCADE,
        related_name="file_message",
    )

    objects: FileMessageManager = FileMessageManager()

    class Meta:
        db_table = "file_message"