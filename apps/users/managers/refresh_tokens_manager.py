from datetime import timezone
from django.db import models
from uuid import UUID

class RefreshTokenManager(models.Manager):
    """Manager for Refresh Token model"""

    def create_token(self, user, refresh_token, expires_in):
        return self.create(
            user=user,
            refresh_token=refresh_token,
            expires_in=expires_in,
        )
    
    def get_valid(self, refresh_token):
        return self.filter(
            refresh_token=refresh_token,
            revoked_at__isnull=True,
            expires_in__gt=timezone.now(),
        ).first()

    def revoke(self, refresh_token):
        return self.filter(
            refresh_token=refresh_token,
            revoked_at__isnull=True,
        ).update(
            revoked_at=timezone.now()
        )

    def revoke_all(self, user_id: UUID):
        return self.filter(
            user=user_id,
            revoked_at__isnull=True,
        ).update(
            revoked_at=timezone.now()
        )