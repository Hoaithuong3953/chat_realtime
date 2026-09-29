from datetime import datetime, timedelta
from uuid import UUID
from django.utils import timezone

from core.redis.client import redis_client
from core.redis.scripts import AI_LIMIT_SCRIPT
from shared.exceptions.ai import AIDailyLimitExceededException
from apps.ai_requests.constants import (
    DAILY_KEY_PREFIX,
    DAILY_LIMIT,
)

class AILimitService:

    @staticmethod
    def consume(user_id: UUID) -> None:
        now = timezone.localtime()
        today = now.date()

        daily_key = f"{DAILY_KEY_PREFIX}:{user_id}:{today.isoformat()}"
        daily_ttl = AILimitService._seconds_until_next_day(now)

        script = redis_client.register_script(AI_LIMIT_SCRIPT)

        result = script(
            keys=[daily_key],
            args=[
                DAILY_LIMIT,
                daily_ttl,
            ],
        )

        if result == 1:
            raise AIDailyLimitExceededException()

    @staticmethod
    def _seconds_until_next_day(now: datetime) -> int:
        next_day = (now + timedelta(days=1)).replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
        )

        return max(1, int((next_day - now).total_seconds()))