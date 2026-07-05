from django.db import IntegrityError, transaction

from apps.users.exception import DuplicateUserException
from apps.users.models import User
from apps.users.dto import (
    RegisterRequest,
    RegisterResponse,
)
from shared.logging import get_logger

logger = get_logger(__name__)

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

            return RegisterResponse.model_validate(user)

        except IntegrityError as e:
            if "email" in str(e):
                raise DuplicateUserException("email")
            if "username" in str(e):
                raise DuplicateUserException("username")
        except Exception as e:
            logger.exception(f"Unexpected error in register user: {str(e)}")
            raise