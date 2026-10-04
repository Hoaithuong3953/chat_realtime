from unittest.mock import patch
import pytest
from django.db import IntegrityError

from apps.accounts.dtos.register_dto import RegisterRequest
from apps.accounts.enums import Role
from apps.accounts.models import Account
from apps.accounts.services.register_service import RegisterService
from apps.users.models import User
from shared.exceptions.auth import (
    EmailAlreadyExistsException,
    UsernameAlreadyExistsException,
)
from .constants import (
    ACCOUNT_EMAIL_UNIQUE_CONSTRAINT,
    ACCOUNT_USERNAME_UNIQUE_CONSTRAINT,
    UNEXPECTED_INTEGRITY_ERROR_MESSAGE,
    USER_CREATION_INTEGRITY_ERROR_MESSAGE,
    TEST_EMAIL,
    TEST_FULL_NAME,
    TEST_PASSWORD,
    TEST_USERNAME,
    EXISTING_EMAIL,
    EXISTING_USERNAME,
    NEW_EMAIL,
    NEW_USERNAME,
)

@pytest.mark.django_db
class TestRegisterService:
    def test_register_success(self):
        """Test that a new account and user profile are created successfully"""
        dto = RegisterRequest(
            email=TEST_EMAIL,
            username=TEST_USERNAME,
            password=TEST_PASSWORD,
            full_name=TEST_FULL_NAME,
        )

        response = RegisterService.register(dto)

        account = Account.objects.get(email=TEST_EMAIL)
        user = User.objects.get(account=account)

        # Response
        assert response.id == account.id
        assert response.email == TEST_EMAIL
        assert response.username == TEST_USERNAME
        assert response.full_name == TEST_FULL_NAME
        assert response.role == Role.USER
        assert response.is_active is True
        assert response.created_at == account.created_at

        # Account
        assert account.email == TEST_EMAIL
        assert account.username == TEST_USERNAME
        assert account.role == Role.USER
        assert account.is_active is True

        # Password
        assert account.password != TEST_PASSWORD
        assert account.check_password(TEST_PASSWORD)

        # User profile
        assert user.account_id == account.id
        assert user.full_name == TEST_FULL_NAME

    def test_register_duplicate_email(self):
        """Test that registration fails when the email already exists"""
        Account.objects.create_account(
            email=TEST_EMAIL,
            username=EXISTING_USERNAME,
            password=TEST_PASSWORD,
        )

        dto = RegisterRequest(
            email=TEST_EMAIL,
            username=NEW_USERNAME,
            password=TEST_PASSWORD,
            full_name=TEST_FULL_NAME,
        )

        with pytest.raises(EmailAlreadyExistsException):
            RegisterService.register(dto)

        assert Account.objects.filter(email=TEST_EMAIL).count() == 1
        assert not Account.objects.filter(username=NEW_USERNAME).exists()
        assert not User.objects.filter(full_name=TEST_FULL_NAME).exists()

    def test_register_duplicate_username(self):
        """Test that registration fails when the username already exists"""
        Account.objects.create_account(
            email=EXISTING_EMAIL,
            username=TEST_USERNAME,
            password=TEST_PASSWORD,
        )

        dto = RegisterRequest(
            email=NEW_EMAIL,
            username=TEST_USERNAME,
            password=TEST_PASSWORD,
            full_name=TEST_FULL_NAME,
        )

        with pytest.raises(UsernameAlreadyExistsException):
            RegisterService.register(dto)

        assert Account.objects.filter(username=TEST_USERNAME).count() == 1
        assert not Account.objects.filter(email=NEW_EMAIL).exists()
        assert not User.objects.filter(full_name=TEST_FULL_NAME).exists()

    @patch("apps.accounts.services.register_service.Account.objects.create_account")
    def test_register_integrity_error_email(self, mock_create_account):
        """Test that an email unique constraint error is converted to an email exception"""
        mock_create_account.side_effect = IntegrityError(
            ACCOUNT_EMAIL_UNIQUE_CONSTRAINT,
        )

        dto = RegisterRequest(
            email=TEST_EMAIL,
            username=TEST_USERNAME,
            password=TEST_PASSWORD,
            full_name=TEST_FULL_NAME,
        )

        with pytest.raises(EmailAlreadyExistsException):
            RegisterService.register(dto)

        mock_create_account.assert_called_once_with(
            email=TEST_EMAIL,
            username=TEST_USERNAME,
            password=TEST_PASSWORD,
        )

    @patch("apps.accounts.services.register_service.Account.objects.create_account")
    def test_register_integrity_error_username(self, mock_create_account):
        """Test that a username unique constraint error is converted to a username exception"""
        mock_create_account.side_effect = IntegrityError(
            ACCOUNT_USERNAME_UNIQUE_CONSTRAINT,
        )

        dto = RegisterRequest(
            email=TEST_EMAIL,
            username=TEST_USERNAME,
            password=TEST_PASSWORD,
            full_name=TEST_FULL_NAME,
        )

        with pytest.raises(UsernameAlreadyExistsException):
            RegisterService.register(dto)

        mock_create_account.assert_called_once_with(
            email=TEST_EMAIL,
            username=TEST_USERNAME,
            password=TEST_PASSWORD,
        )

    @patch("apps.accounts.services.register_service.Account.objects.create_account")
    def test_register_unexpected_integrity_error_is_reraised(self, mock_create_account):
        """Test that unexpected integrity errors are re-raised unchanged"""
        error = IntegrityError(
            UNEXPECTED_INTEGRITY_ERROR_MESSAGE,
        )
        mock_create_account.side_effect = error

        dto = RegisterRequest(
            email=TEST_EMAIL,
            username=TEST_USERNAME,
            password=TEST_PASSWORD,
            full_name=TEST_FULL_NAME,
        )

        with pytest.raises(IntegrityError) as exc_info:
            RegisterService.register(dto)

        assert exc_info.value is error

    @patch("apps.accounts.services.register_service.User.objects.create")
    def test_register_user_creation_integrity_error_rolls_back_account(self, mock_create_user):
        """Test that account creation is rolled back when user creation fails"""
        mock_create_user.side_effect = IntegrityError(
            USER_CREATION_INTEGRITY_ERROR_MESSAGE,
        )

        dto = RegisterRequest(
            email=TEST_EMAIL,
            username=TEST_USERNAME,
            password=TEST_PASSWORD,
            full_name=TEST_FULL_NAME,
        )

        with pytest.raises(IntegrityError):
            RegisterService.register(dto)

        assert not Account.objects.filter(email=TEST_EMAIL).exists()
        assert not User.objects.filter(full_name=TEST_FULL_NAME).exists()