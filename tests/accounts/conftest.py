import pytest
from django.utils import timezone
from datetime import timedelta
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken

from apps.accounts.models import Account, RefreshToken
from apps.users.models import User
from shared.security import TokenHasher
from .constants import (
    TEST_EMAIL,
    TEST_PASSWORD,
    TEST_USERNAME,
    VALID_REFRESH_TOKEN,
    REFRESH_TOKEN_EXPIRES_DAYS,
)

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def account():
    return Account.objects.create_account(
        email=TEST_EMAIL,
        username=TEST_USERNAME,
        password=TEST_PASSWORD,
    )

@pytest.fixture
def account_factory():
    def create_account(
        email="account@example.com",
        username="account",
        role=None,
        is_active=True,
        full_name="Test User",
        avatar_url=None,
    ):
        data = {
            "email": email,
            "username": username,
            "is_active": is_active,
        }

        if role is not None:
            data["role"] = role

        account = Account.objects.create(**data)

        User.objects.create(
            account=account,
            full_name=full_name,
            avatar_url=avatar_url,
        )

        return account

    return create_account

@pytest.fixture
def refresh_token(account):
    RefreshToken.objects.create_token(
        account=account,
        refresh_token=TokenHasher.hash_token(VALID_REFRESH_TOKEN),
        expires_in=timezone.now() + timedelta(
            days=REFRESH_TOKEN_EXPIRES_DAYS,
        ),
    )
    return VALID_REFRESH_TOKEN

@pytest.fixture
def access_token(account):
    return str(AccessToken.for_user(account))