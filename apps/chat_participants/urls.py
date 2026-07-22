from django.urls import path
# from apps.chat_participants.views import
from apps.chat_participants.views import GroupMemberView

urlpatterns = [
    path("members", GroupMemberView.as_view(), name="member-group"),
]