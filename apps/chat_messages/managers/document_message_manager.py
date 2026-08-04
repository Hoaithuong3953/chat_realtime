from uuid import UUID

from django.db import models
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from apps.chat_messages.models import DocumentMessage

class DocumentMessageManager(models.Manager["DocumentMessage"]):
    """
    Manager for Document Message model

    Provides method for manager document message
    """
    def create_document_message(
        self,
        chat_id: UUID,
        file_asset_id: UUID,
    ):
        """Add document message"""
        return self.create(
            chat_id=chat_id,
            file_asset_id=file_asset_id,
        )