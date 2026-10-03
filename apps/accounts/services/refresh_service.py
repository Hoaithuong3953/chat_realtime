from django.utils import timezone
from rest_framework_simplejwt.tokens import AccessToken
from django.db import transaction

from apps.accounts.dtos import RefreshTokenResponse
from apps.accounts.models import RefreshToken
from shared.exceptions.auth import InvalidRefreshTokenException
from shared.security import TokenHasher, RefreshTokenService

class RefreshService:

    @staticmethod
    @transaction.atomic
    def refresh(refresh_token: str) -> RefreshTokenResponse:
        if not refresh_token:
            raise InvalidRefreshTokenException()
        
        hashed_refresh_token  = TokenHasher.hash_token(refresh_token)

        refresh = RefreshToken.objects.find_active_by_hash(hashed_refresh_token)

        if refresh is None:
            raise InvalidRefreshTokenException()

        if refresh.expires_in <= timezone.now():
            raise InvalidRefreshTokenException()

        new_refresh_token = RefreshTokenService.generate_refresh_token()

        RefreshToken.objects.rotate_token(
            account_id=refresh.account_id,
            refresh_token=TokenHasher.hash_token(new_refresh_token ),
            expires_in=RefreshTokenService.get_refresh_expiration(),
        )

        access_token = AccessToken.for_user(refresh.account)

        expires_in = int(access_token.lifetime.total_seconds())

        return RefreshTokenResponse(
            access_token=str(access_token),
            expires_in=expires_in,
            refresh_token=new_refresh_token,
        )