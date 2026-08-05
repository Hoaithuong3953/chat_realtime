from django.urls import path
from apps.chat_messages.views import (
    MessageView,
    MessageRecallView,
    DocumentMessageView
)

urlpatterns = [
    path("messages", MessageView.as_view(), name="messages"),
    path("messages/<uuid:message_id>/recall", MessageRecallView.as_view(), name="recall-message"),
    path("messages/document", DocumentMessageView.as_view(), name="document-message"),
]