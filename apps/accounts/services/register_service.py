from django.db import IntegrityError, transaction

from shared.exceptions.auth import EmailAlreadyExistsException, UsernameAlreadyExistsException
from apps.accounts.dtos.register_dto import RegisterRequest, RegisterResponse
from apps.accounts.models import Account
from apps.users.models import User

class RegisterService:
    """
    Service layer for registration a new user
    """
    @staticmethod
    @transaction.atomic
    def register(dto: RegisterRequest) -> RegisterResponse:
        """
        Register a new user account

        Raises:
            EmailAlreadyExistsException: If the email is already in use
            UsernameAlreadyExistsException: If the username is already in use
        """
        if Account.objects.email_exists(dto.email):
            raise EmailAlreadyExistsException()

        if Account.objects.username_exists(dto.username):
            raise UsernameAlreadyExistsException()

        try:
            account = Account.objects.create_account(
                email=dto.email,
                username=dto.username,
                password=dto.password,
            )

            user = User.objects.create(
                account=account,
                full_name=dto.full_name,
            )

        except IntegrityError as e:
            if "email" in str(e):
                raise EmailAlreadyExistsException()
            if "username" in str(e):
                raise UsernameAlreadyExistsException()
            
        return RegisterResponse(
            id=account.id,
            email=account.email,
            username=account.username,
            full_name=user.full_name,
            role=account.role,
            is_active=account.is_active,
            created_at=account.created_at,
        )