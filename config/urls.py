"""
URL configuration for backend project.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/v1/auth/",
        include("apps.accounts.urls"),
    ),
    path(
        "api/v1/users/",
        include("apps.users.urls")
    ),
    path(
        "api/v1/chats/",
        include("apps.chats.urls")
    ),
    path(
        "api/v1/chats/group/<uuid:chat_id>/",
        include("apps.chat_participants.urls")
    ),
    path(
        "api/v1/chats/<uuid:chat_id>/",
        include("apps.chat_messages.urls")
    ),
]
