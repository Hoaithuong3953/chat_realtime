from django.urls import path
from apps.chat_participants.views import (
    GroupMemberView,
    DeleteGroupMemberView,
    TransferOwnershipView,
)

urlpatterns = [
    path("members", GroupMemberView.as_view(), name="member-group"),
    path("members/<uuid:member_id>", DeleteGroupMemberView.as_view(), name="delete-member"),
    path("members/owner", TransferOwnershipView.as_view(), name="transfer-ownership"),
]