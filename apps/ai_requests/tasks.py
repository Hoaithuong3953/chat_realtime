from uuid import UUID
from celery import shared_task

from apps.ai_requests.services.ai_worker import AIWorker
from core.ai.retry_policy import AIRetryPolicy
from apps.ai_requests.constants import (
    RETRY_DELAYS,
    CELERY_TIME_LIMIT,
)

@shared_task(bind=True, time_limit=CELERY_TIME_LIMIT)
def process_ai_request(self, request_id: str, input: str) -> None:
    request_uuid = UUID(request_id)

    try:
        AIWorker.process(request_id=request_uuid, input=input)

    except Exception as exc:
        if not AIRetryPolicy.is_retryable(exc):
            AIWorker.mark_failed(
                request_id=request_uuid,
                error_message=str(exc),
            )
            raise

        retry_number = self.request.retries

        if retry_number >= len(RETRY_DELAYS):
            AIWorker.mark_failed(
                request_id=request_uuid,
                error_message=str(exc),
            )
            raise

        raise self.retry(
            exc=exc,
            countdown=RETRY_DELAYS[retry_number],
        )