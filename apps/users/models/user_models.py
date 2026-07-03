from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from shared.database.models import BaseSoftDeleteModel
from .user_manager import UserManager
from apps.users.constants import UserRole

class User(BaseSoftDeleteModel, AbstractBaseUser, PermissionsMixin):
    """Custom User model"""
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    role = models.CharField(
        max_length=10,
        choices=UserRole.choices,
        default=UserRole.USER,
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "name"]

    class Meta:
        db_table = "user"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.email} ({self.username})"