from django.db import models
from django.conf import settings

from apps.users.user_manager import UserManager
from apps.users.constants import (
    FULL_NAME_MAX_LENGTH,
    AVATAR_URL_MAX_LENGTH,
    PHONE_NUMBER_MAX_LENGTH,
    ADDRESS_MAX_LENGTH,
    BIO_MAX_LENGTH,
)
from shared.base_models import BaseSoftDeleteModel

class User(BaseSoftDeleteModel):
    """
    Represents the profile information associated with an account
    """
    account = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_profile",
    )
    full_name = models.CharField(max_length=FULL_NAME_MAX_LENGTH)
    avatar_url = models.URLField(max_length=AVATAR_URL_MAX_LENGTH, blank=True, null=True)
    phone_number = models.CharField(max_length=PHONE_NUMBER_MAX_LENGTH, blank=True, null=True)
    address = models.CharField(max_length=ADDRESS_MAX_LENGTH, blank=True, null=True)
    dob = models.DateField(null=True, blank=True)
    bio = models.TextField(max_length=BIO_MAX_LENGTH, blank=True, null=True)

    objects = UserManager()

    class Meta:
        db_table = "users"
        ordering = ["-created_at"]

    def __str__(self):
        return self.full_name