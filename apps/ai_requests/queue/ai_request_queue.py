from uuid import UUID

from .tasks import process_ai_request

class AIRequestQueue:

    @staticmethod
    def enqueue(request_id: UUID) -> None:
        process_ai_request.delay(str(request_id))