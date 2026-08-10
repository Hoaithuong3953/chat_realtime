from django.urls import path
from apps.chat_messages.views import (
    MessageView,
    MessageRecallView,
    FileMessageView,
)

urlpatterns = [
    path("messages", MessageView.as_view(), name="messages"),
    path("messages/<uuid:message_id>/recall", MessageRecallView.as_view(), name="recall-message"),
    path("messages/file", FileMessageView.as_view(), name="file-message"),
]