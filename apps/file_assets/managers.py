from typing import TYPE_CHECKING
from uuid import UUID
from django.db import models

from apps.file_assets.enums import FileStatus

if TYPE_CHECKING:
    from apps.file_assets.models import FileAsset

class FileAssetManager(models.Manager["FileAsset"]):

    def create_file(
        self,
        user_id: str,
        storage_key: str,
        original_name: str,
        content_type: str,
        file_size: int,
        status: FileStatus,
    ):
        """Add a record when upload file"""
        return self.create(
            user_id=user_id,
            storage_key=storage_key,
            original_name=original_name,
            content_type=content_type,
            file_size=file_size,
            status=status,
        )

    def get_active_by_ids(self, file_ids: list[UUID]):
        """Get active file by list of IDs"""
        return self.filter(
            id__in=file_ids,
            deleted_at__isnull=True,
        )