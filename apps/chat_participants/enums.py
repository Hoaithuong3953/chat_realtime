"""
Enumrations used by the chat participant module
"""
from django.db import models

class ParticipantRole(models.TextChoices):
    """Available role for chat"""
    OWNER = "OWNER", "owner"
    MEMBER = "MEMBER", "member"