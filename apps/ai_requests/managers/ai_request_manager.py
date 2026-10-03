from typing import TYPE_CHECKING
from uuid import UUID
from django.db import models
from django.db.models import F

from apps.ai_requests.enums import AIRequestStatus

if TYPE_CHECKING:
    from apps.ai_requests.models import AIRequest

class AIRequestManager(models.Manager["AIRequest"]):

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
        return (
            self.select_related("input_message__chat")
            .filter(id=request_id)
            .first()
        )
    
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

    def increment_attempt_count(self, request_id: UUID) -> None:
        self.filter(id=request_id).update(
            attempt_count=F("attempt_count") + 1,
        )

    def get_for_update(self, request_id: UUID):
        return self.select_for_update().get(id=request_id)