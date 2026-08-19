from django.db import models

from shared.base_models import BaseModel
from apps.ai_requests.enums import AIRequestStatus
from apps.ai_requests.constants import STATUS_MAX_LENGTH, ERROR_MESSAGE_MAX_LENGTH, MODEL_MAX_LENGTH

class AIRequest(BaseModel):
    """Represents the request to AI service"""
    input_message = models.ForeignKey(
        "chat_messages.Message",
        on_delete=models.CASCADE,
        related_name="ai_requests",
    )
    output_message = models.ForeignKey(
        "chat_messages.Message",
        on_delete=models.SET_NULL,
        related_name="ai_output_requests",
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=STATUS_MAX_LENGTH,
        choices=AIRequestStatus,
        default=AIRequestStatus.PROCESSING,
    )
    error_message = models.CharField(
        max_length=ERROR_MESSAGE_MAX_LENGTH,
        null=True,
        blank=True,
    )
    model = models.CharField(max_length=MODEL_MAX_LENGTH)

    class Meta:
        db_table = "ai_request"