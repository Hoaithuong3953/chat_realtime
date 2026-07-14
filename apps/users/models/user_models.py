from django.db import models
from django.conf import settings

from shared.database.models import BaseSoftDeleteModel

class User(BaseSoftDeleteModel):
    """
    Represents the profile information associated with an account
    """
    account = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_profile",
    )
    full_name = models.CharField(max_length=100)
    avatar_url = models.URLField(max_length=500, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    dob = models.DateField(null=True, blank=True)
    bio = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "user"
        ordering = ["-created_at"]

    def __str__(self):
        return self.full_name