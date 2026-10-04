import pytest
from rest_framework.test import APIClient

from apps.accounts.models import Account
from .constants import (
    TEST_EMAIL,
    TEST_PASSWORD,
    TEST_USERNAME,
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