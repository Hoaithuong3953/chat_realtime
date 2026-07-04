from django.db import transaction
from rest_framework.exceptions import ValidationError

from apps.users.exception import DuplicateUserException
from apps.users.models import User
from apps.users.serializers import RegisterSerializer
from apps.users.dto import RegisterRequest, RegisterResponse
from shared.logging import get_logger

logger = get_logger(__name__)

class AuthService:
    """Service layer for authentication business logic"""

    @staticmethod
    def register_user(request: RegisterRequest) -> RegisterResponse:
        """
        Register new user and return success response
        Raises ValidationError for business errors
        """
        logger.debug(f"Register user started with data: {request}")

        try:
            # Validate data
            serializer = RegisterSerializer(data=request)
            serializer.is_valid(raise_exception=True)
            validated_data = serializer.validated_data

            email = validated_data["email"]
            username = validated_data["username"]
            password = validated_data['password']
            name = validated_data['name']

            with transaction.atomic():
                if User.objects.email_exists(email):
                    logger.warning(f"Duplicate email: {email}")
                    raise DuplicateUserException(field=email)
                
                if User.objects.username_exists(username):
                    logger.warning(f"Duplicate username: {username}")
                    raise DuplicateUserException(field=username)

                user = User.objects.create_user(
                    email=email,
                    username=username,
                    password=password,
                    name=name
                )

            logger.info(f"User created successfully with id={user.id}, email={user.email}")

            return RegisterResponse(
                id=user.id,
                email=user.email,
                username=user.username,
                name=user.name,
                role=user.role,
                is_active=user.is_active,
                created_at=user.created_at,
            )

        except DuplicateUserException:
            raise
        except ValidationError as e:
            logger.warning(f"Validation failed: {e.detail}")
            raise
        except Exception as e:
            logger.exception(f"Unexpected error in register user: {str(e)}")
            raise