"""
Django settings for project

Key features:
- settings: loaded from environment variables using pydantic settings
"""

from .env import settings

__all__ = ["settings"]