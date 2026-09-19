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
    
    def update_request(self, request_id: UUID, **fields):
        """Update fields of an AI request"""
        return self.filter(
            id=request_id,
        ).update(**fields)

    def claim_request(self, request_id: UUID) -> bool:
        """Claim a queued AI request for processing"""
        updated = self.filter(
            id=request_id,
            status=AIRequestStatus.QUEUED,
        ).update(
            status=AIRequestStatus.PROCESSING,
        )

        return updated==1