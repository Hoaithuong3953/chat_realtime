from django.urls import path
from apps.chats.views import (
    PrivateChatView,
    CreateGroupChatView,
    GroupChatDetailView,
    GetChatListView,
)

urlpatterns = [
    path("private", PrivateChatView.as_view(), name="private_chat"),
    path("group", CreateGroupChatView.as_view(), name="group_chat_create"),
    path("group/<uuid:chat_id>", GroupChatDetailView.as_view(), name="group_chat_detail"),
    path("", GetChatListView.as_view(), name="chat-list"),
]