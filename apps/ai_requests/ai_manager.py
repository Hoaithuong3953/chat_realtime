from typing import TYPE_CHECKING
from uuid import UUID
from django.db import models

from apps.ai_requests.enums import AIRequestStatus

if TYPE_CHECKING:
    from apps.ai_requests.models import AIRequest

class AIManager(models.Manager["AIRequest"]):

    def create_request(
        self,
        input_message_id: UUID,
        status: AIRequestStatus,
        model: str,
    ):
        """Create an AI request"""
        return self.create(
            input_message_id=input_message_id,
            status=status,
            model=model,
        )

    def get_by_id(self, request_id: UUID):
        """Find request by id"""
        return self.filter(id=request_id).first()