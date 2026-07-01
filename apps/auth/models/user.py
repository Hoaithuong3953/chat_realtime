from django.db import models

from shared.database.models import BaseModel

class UserRole(models.TextChoices):
    ADMIN = "admin", "Admin", "ADMIN"
    USER = "user", "User", "USER"

class User(BaseModel):
    """
    User model for authentication and authorization
    """
    email = models.EmailField(unique=True, max_length=255)
    username = models.CharField(unique=True, max_length=50)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=100)
    role = models.CharField(
        max_length=10,
        choices=UserRole.choices,
        default=UserRole.USER
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "users"