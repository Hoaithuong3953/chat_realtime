from django.db import transaction
from django.contrib.auth.hashers import check_password

from apps.users.exception import InvalidCredentialsException
from apps.users.models import User, RefreshToken
from apps.users.dto import (
    LoginRequest,
    LoginResponse,
)
from shared.security import (
    JWTService,
    RefreshTokenService,
    TokenHasher
)

class AuthService:
    """Service layer for authentication business logic"""
    
    @staticmethod
    @transaction.atomic
    def login(request: LoginRequest) -> LoginResponse:
        user = User.objects.get_by_identify(
            request.identifier,
        )

        if user is None:
            raise InvalidCredentialsException()
        
        if not check_password(request.password, user.password):
            raise InvalidCredentialsException()
        
        access_token = JWTService.generate_access_token(user_id=user.id)
        refresh_token = RefreshTokenService.generate_refresh_token()

        RefreshToken.objects.upsert_token(
            user=user,
            refresh_token=TokenHasher.hash_token(refresh_token),
            expires_in=RefreshTokenService.get_refresh_expiration(),
        )

        return LoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
        )