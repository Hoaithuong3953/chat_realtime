"""
Enumrations used by the chat module
"""
from django.db import models

class ChatType(models.TextChoices):
    """Available type for chat"""
    DIRECT = "DIRECT", "direct"
    GROUP = "GROUP", "group"

class ChatRole(models.TextChoices):
    """Available role for chat"""
    OWNER = "OWNER", "owner"
    MEMBER = "MEMBER", "member"