from django.db import models

from apps.chat_messages.managers import DocumentMessageManager

class DocumentMessage(models.Model):
    """Link a message with a document attachment"""
    message = models.OneToOneField(
        "chat_messages.Message",
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="document_message",
    )
    file_asset = models.ForeignKey(
        "file_assets.FileAsset",
        on_delete=models.CASCADE,
        related_name="document_message",
    )

    objects: DocumentMessageManager = DocumentMessageManager()

    class Meta:
        db_table = "document_message"