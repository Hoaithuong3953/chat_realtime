from django.db import models

from shared.base_models import BaseSoftDeleteModel
from apps.file_assets.enums import FileStatus
from apps.file_assets.constants import (
    STORAGE_KEY_MAX_LENGTH,
    ORIGINAL_NAME_MAX_LENGTH,
    CONTENT_TYPE_MAX_LENGTH,
    STATUS_MAX_LENGTH,
)
from apps.file_assets.managers import FileAssetManager

class FileAsset(BaseSoftDeleteModel):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="file_assets",
    )
    storage_key = models.CharField(max_length=STORAGE_KEY_MAX_LENGTH, unique=True)
    original_name = models.CharField(max_length=ORIGINAL_NAME_MAX_LENGTH)
    content_type = models.CharField(max_length=CONTENT_TYPE_MAX_LENGTH)
    file_size = models.BigIntegerField()
    status = models.CharField(
        max_length=STATUS_MAX_LENGTH,
        choices=FileStatus.choices,
        default=FileStatus.PENDING,
    )

    def __str__(self):
        return f"{self.original_name} ({self.storage_key})"

    objects: FileAssetManager = FileAssetManager()

    class Meta:
        db_table = "file_assets"