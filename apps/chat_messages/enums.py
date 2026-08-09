"""
Enumrations used by the message module
"""
from django.db import models

class MessageType(models.TextChoices):
    """Available type for message"""
    TEXT = "TEXT", "text"
    DOCUMENT = "DOCUMENT", "document"
    IMAGE = "IMAGE", "image"

class MessageStatus(models.TextChoices):
    """Available status for message"""
    ACTIVE = "ACTIVE", "active"
    RECALLED = "RECALLED", "recalled"