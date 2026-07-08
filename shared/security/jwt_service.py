from django.utils import timezone
import jwt

from shared.config.jwt import jwt_config

class JWTService:
    """Creates and validates JWT access tokens"""
    ACCESS_TOKEN_LIFETIME = jwt_config.access_lifetime
    JWT_ALGORITHM = jwt_config.algorithm

    @classmethod
    def generate_access_token(cls, user_id) -> str:
        """Generate a signed JWT access token"""
        now = timezone.now()

        payload = {
            "sub": str(user_id),
            "type": "access",
            "iat": now,
            "exp": now + cls.ACCESS_TOKEN_LIFETIME,
        }

        return jwt.encode(
            payload=payload,
            key=jwt_config.secret_key,
            algorithm=cls.JWT_ALGORITHM,
        )
    
    @classmethod
    def decode_access_token(cls, token: str) -> dict:
        """Decode and validate an access token"""
        return jwt.decode(
            jwt=token,
            key=jwt_config.secret_key,
            algorithms=[cls.JWT_ALGORITHM],
        )
    
    