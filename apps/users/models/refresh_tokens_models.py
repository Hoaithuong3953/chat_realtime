from django.db import models

from shared.database.models import BaseModel
from .user_models import User
from apps.users.managers import RefreshTokenManager

class RefreshToken(BaseModel):
    """Refresh Token model"""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        unique=True,
    )
    refresh_token = models.CharField(max_length=255, unique=True)
    expires_in = models.DateTimeField()
    revoked_at = models.DateTimeField(null=True, blank=True)

    objects = RefreshTokenManager()

    class Meta:
        db_table = "refresh_tokens"

    def __str__(self):
        return str(self.user_id)