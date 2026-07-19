"""
Enumrations used by the message module
"""
from django.db import models

class MessageType(models.TextChoices):
    """Available type for message"""
    TEXT = "TEXT", "text"
    SYSTEM = "SYSTEM", "system"
    FILE = "FILE", "file"
    AI = "AI", "ai"