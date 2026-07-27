from django.urls import path
from apps.chat_messages.views import (
    MessageView,
    MessageRecallView,
)

urlpatterns = [
    path("messages", MessageView.as_view(), name="messages"),
    path("messages/<uuid:message_id>/recall", MessageRecallView.as_view(), name="recall-message"),
]