from django.db import models

from shared.base_models import BaseModel
from apps.accounts.models import Account
from apps.accounts.managers import RefreshTokenManager

class RefreshToken(BaseModel):
    """Refresh Token model"""
    account = models.OneToOneField(
        Account,
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
        return str(self.account.id)