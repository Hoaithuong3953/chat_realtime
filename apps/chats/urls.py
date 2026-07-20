from django.urls import path
from apps.chats.views import PrivateChatView, CreateGroupChatView

urlpatterns = [
    path("private", PrivateChatView.as_view(), name="private_chat"),
    path("group", CreateGroupChatView.as_view(), name="group_chat_create"),
]