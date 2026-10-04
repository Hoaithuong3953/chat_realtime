from django.db import transaction
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.tokens import AccessToken

from shared.exceptions.auth import InvalidCredentialsException, AccountDisabledException
from apps.accounts.dtos import LoginRequest, LoginResponse
from apps.accounts.models import Account, RefreshToken
from shared.security import (
    RefreshTokenService,
    TokenHasher
)

class LoginService:
    """
    Service layer for authentication a user
    """
    @staticmethod
    @transaction.atomic
    def login(dto: LoginRequest) -> LoginResponse:
        """
        Authenticate a user and return the login result

        Args:
            dto: Login credentials

        Returns:
            The generated access and refresh tokens

        Raises:
            InvalidCredentialsException: If the credentials are invalid
            AccountDisabledException: If the account is inactive
        """
        account = Account.objects.get_by_identifier(
            dto.identifier,
        )

        if account is None:
            raise InvalidCredentialsException()

        if not account.check_password(dto.password):
            raise InvalidCredentialsException()
        
        if not account.is_active:
            raise AccountDisabledException()
        
        access_token = str(AccessToken.for_user(account))
        refresh_token = RefreshTokenService.generate_refresh_token()

        RefreshToken.objects.upsert_token(
            account=account,
            refresh_token=TokenHasher.hash_token(refresh_token),
            expires_in=RefreshTokenService.get_refresh_expiration(),
        )

        update_last_login(None, account)

        return LoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
        )