"""
Export views for Message module
"""
from .message_view import MessageView
from .message_recall_view import MessageRecallView

__all__ = [
    "MessageView",
    "MessageRecallView",
]