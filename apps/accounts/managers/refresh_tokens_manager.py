from __future__ import annotations
from typing import TYPE_CHECKING
from django.db import models
from django.utils import timezone

if TYPE_CHECKING:
    from apps.accounts.models import RefreshToken

class RefreshTokenManager(models.Manager["RefreshToken"]):
    """Manager for Refresh Token model"""

    def create_token(self, account, refresh_token, expires_in):
        return self.create(
            account=account,
            refresh_token=refresh_token,
            expires_in=expires_in,
        )
    
    def upsert_token(self, account, refresh_token, expires_in):
        return self.update_or_create(
            account=account,
            defaults={
                "refresh_token": refresh_token,
                "expires_in": expires_in,
                "revoked_at": None,
            }
        )
    
    def find_active_by_hash(self, refresh_token):
        return (
            self.select_related("account")
            .filter(
                refresh_token=refresh_token,
                revoked_at__isnull=True,
            )
            .first()
        )
    
    def rotate_token(self, account_id, refresh_token, expires_in):
        return self.filter(
            account_id=account_id,
        ).update(
            refresh_token=refresh_token,
            expires_in=expires_in,
            revoked_at=None,
        )
    
    def revoke_by_hash(self, refresh_token):
        return (
            self.filter(
                refresh_token=refresh_token,
                revoked_at__isnull=True,
            )
            .update(
                revoked_at=timezone.now(),
            )
        )