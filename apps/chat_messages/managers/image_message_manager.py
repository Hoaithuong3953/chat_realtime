from uuid import UUID
from django.db import models
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from apps.chat_messages.models import ImageMessage

class ImageMessageManager(models.Manager["ImageMessage"]):
    """
    Manager for Image Message model

    Provides method for manager image message
    """
    def create_image_messages(
        self,
        message_id: UUID,
        asset_ids: list[UUID],
    ):
        """Add multiple image messages to a message"""
        image_messages = []
        for position, asset_id in enumerate(asset_ids):
            image_messages.append(
                self.model(
                    message_id=message_id,
                    asset_id = asset_id,
                    position = position,
                )
            )

        return self.bulk_create(image_messages)