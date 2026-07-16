import uuid
from django.db import models
from django.utils.timezone import now

class BaseModel(models.Model):
    """
    Base model for all database models
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']

class BaseSoftDeleteModel(BaseModel):
    """
    Base model with soft delete support
    """
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None

    def soft_delete(self):
        self.deleted_at = now()
        self.save(update_fields=["deleted_at", "updated_at"])