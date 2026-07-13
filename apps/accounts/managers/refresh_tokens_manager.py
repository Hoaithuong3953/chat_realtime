from django.db import models

class RefreshTokenManager(models.Manager):
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