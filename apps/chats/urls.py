from django.urls import path
from apps.chats.views import PrivateChatView

urlpatterns = [
    path("private", PrivateChatView.as_view(), name="private_chat"),
]