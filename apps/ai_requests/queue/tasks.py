from uuid import UUID
from celery import shared_task

from apps.ai_requests.services import AIWorker

@shared_task
def process_ai_request(request_id: str) -> None:
    AIWorker.process(request_id=UUID(request_id))