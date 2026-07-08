"""
Enumrations used by the auth module
"""
from django.db import models

class Role(models.TextChoices):
    """Available roles for accounts"""
    ADMIN = "ADMIN", "admin"
    USER = "USER", "user"