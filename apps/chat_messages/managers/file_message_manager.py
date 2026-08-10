from uuid import UUID
from django.db import models
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from apps.chat_messages.models import FileMessage

class FileMessageManager(models.Manager["FileMessage"]):
    """
    Manager for File message model

    Provides method for manager file message
    """
    def create_file_message(
        self,
        message_id: UUID,
        file_asset_id: UUID,
    ):
        """Add file message"""
        return self.create(
            message_id=message_id,
            file_asset_id=file_asset_id,
        )