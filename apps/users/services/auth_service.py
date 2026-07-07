from django.db import IntegrityError, transaction
from django.contrib.auth.hashers import check_password

from apps.users.exception import DuplicateUserException, InvalidCredentialsException
from apps.users.models import User, RefreshToken
from apps.users.dto import (
    RegisterRequest,
    RegisterResponse,
    LoginRequest,
    LoginResponse,
)
from .jwt_service import JWTService
from .refresh_token_service import RefreshTokenService
from shared.security.token_hasher import TokenHasher

class AuthService:
    """Service layer for authentication business logic"""

    @staticmethod
    @transaction.atomic
    def register_user(request: RegisterRequest) -> RegisterResponse:
        """
        Register new user and return success response
        Raises ValidationError for business errors
        """
        if User.objects.email_exists(request.email):
            raise DuplicateUserException("email")

        if User.objects.username_exists(request.username):
            raise DuplicateUserException("username")

        try:
            user = User.objects.create_user(
                email=request.email,
                username=request.username,
                password=request.password,
                name=request.name,
            )

        except IntegrityError as e:
            if "email" in str(e):
                raise DuplicateUserException("email")
            if "username" in str(e):
                raise DuplicateUserException("username")
            
        return RegisterResponse.model_validate(user)
    
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