from django.db import models

class FileStatus(models.TextChoices):
    """Available status for file asset"""
    PENDING = "PENDING", "pending"
    UPLOADED = "UPLOADED", "uploaded"
    FAILED = "FAILED", "failed"