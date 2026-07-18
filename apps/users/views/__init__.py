"""
Export views for User module
"""
from .profile_view import ProfileView
from .user_view import UserView

__all__ = [
    "ProfileView",
    "UserView",
]