"""
Enumrations used by the chat module
"""
from django.db import models

class ChatType(models.TextChoices):
    """Available type for chat"""
    PRIVATE = "PRIVATE", "private"
    GROUP = "GROUP", "group"