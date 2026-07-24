from django.urls import path
from apps.chat_messages.views import (
    MessageView,
)

urlpatterns = [
    path("messages", MessageView.as_view(), name="messages"),
]