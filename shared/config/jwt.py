from dataclasses import dataclass
from datetime import timedelta

from .env import settings

@dataclass(frozen=True)
class JWTConfig:
    secret_key: str
    algorithm: str
    access_lifetime: timedelta
    refresh_lifetime: timedelta

jwt_config = JWTConfig(
    secret_key=settings.JWT_SECRET_KEY,
    algorithm=settings.JWT_ALGORITHM,
    access_lifetime=timedelta(settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    refresh_lifetime=timedelta(settings.REFRESH_TOKEN_EXPIRE_DAYS),
)