from django.utils import timezone
from rest_framework_simplejwt.tokens import AccessToken
from django.db import transaction

from apps.accounts.dtos import RefreshTokenResponse
from apps.accounts.models import RefreshToken
from apps.accounts.exceptions import InvalidRefreshTokenException
from shared.security import TokenHasher, RefreshTokenService

class RefreshService:

    @staticmethod
    @transaction.atomic
    def refresh(refresh_token: str) -> RefreshTokenResponse:
        refresh_token = TokenHasher.hash_token(refresh_token)

        refresh = RefreshToken.objects.find_by_hash(refresh_token)

        if refresh is None:
            raise InvalidRefreshTokenException()

        if refresh.revoked_at is not None:
            raise InvalidRefreshTokenException()

        if refresh.expires_in <= timezone.now():
            raise InvalidRefreshTokenException()

        new_refresh_token = RefreshTokenService.generate_refresh_token()

        RefreshToken.objects.rotate_token(
            account_id=refresh.account_id,
            refresh_token=TokenHasher.hash_token(new_refresh_token ),
            expires_in=RefreshTokenService.get_refresh_expiration(),
        )

        access_token = str(
            AccessToken.for_user(refresh.account)
        )

        return RefreshTokenResponse(
            access_token=access_token,
            refresh_token=new_refresh_token,
        )