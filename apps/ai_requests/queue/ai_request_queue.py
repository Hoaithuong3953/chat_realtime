from uuid import UUID

class AIRequestQueue:

    @staticmethod
    def enqueue(request_id: UUID, input: str) -> None:
        from apps.ai_requests.tasks import process_ai_request

        process_ai_request.delay(str(request_id), input)