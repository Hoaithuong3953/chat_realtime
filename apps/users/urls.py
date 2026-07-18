from django.urls import path
from apps.users.views import ProfileView, UserView

urlpatterns = [
    path("", UserView.as_view(), name="list"),
    path("profile", ProfileView.as_view(), name="profile"),
]