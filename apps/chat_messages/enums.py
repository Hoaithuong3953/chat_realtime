"""
Enumrations used by the message module
"""
from django.db import models

class MessageType(models.TextChoices):
    """Available type for message"""
    TEXT = "TEXT", "text"
    FILE = "FILE", "file"

class MessageStatus(models.TextChoices):
    """Available status for message"""
    ACTIVE = "ACTIVE", "active"
    RECALLED = "RECALLED", "recalled"