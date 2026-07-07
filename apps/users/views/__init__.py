"""
Export views for User module
"""
from .register_view import RegisterView
from .login_view import LoginView

__all__ = [
    "RegisterView",
    "LoginView",
]