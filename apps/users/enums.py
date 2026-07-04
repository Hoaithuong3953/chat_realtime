"""
Enumerations used by the users module
"""
from django.db import models

class UserRole(models.TextChoices):
    """Available roles for users"""
    ADMIN = "ADMIN", "admin"
    USER = "USER", "user"