import hashlib
import hmac

class TokenHasher:
    """Hashes and verifies refresh tokens"""

    @staticmethod
    def hash_token(token: str) -> str:
        """Compute SHA-256 hash for a token"""
        return hashlib.sha256(token.encode("utf-8")).hexdigest()
    
    @staticmethod
    def verify_token(token: str, token_hash: str) -> bool:
        """Verify a raw_token against its hash"""
        return hmac.compare_digest(
            TokenHasher.hash(token),
            token_hash,
        )