from django.db import IntegrityError, transaction

from apps.users.exception import DuplicateUserException
from apps.users.models import User
from apps.users.dto import (
    RegisterRequest,
    RegisterResponse,
)

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