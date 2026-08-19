"""
Enumrations used by the AI requests module
"""
from django.db import models

class AIRequestStatus(models.TextChoices):
    """Available status for AI request"""
    PROCESSING = "PROCESSING", "processing"
    COMPLETED = "COMPLETED", "completed"
    FAILED = "FAILED", "failed"
    QUEUED = "QUEUED", "queued"