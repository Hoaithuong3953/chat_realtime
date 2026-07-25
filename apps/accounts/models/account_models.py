from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from apps.accounts.managers.account_manager import AccountManager
from shared.base_models import BaseSoftDeleteModel
from apps.accounts.enums import Role

class Account(BaseSoftDeleteModel, AbstractBaseUser):
    """
    Custom user model for authentication and authorization
    """
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.USER,
    )
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects: AccountManager = AccountManager()

    class Meta:
        db_table = "accounts"

    def __str__(self):
        return f"{self.email} ({self.username})"