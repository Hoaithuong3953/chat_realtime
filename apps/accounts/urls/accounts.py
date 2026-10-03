from django.urls import path

from apps.accounts.views import AccountView

urlpatterns = [
    path("", AccountView.as_view(), name="account-list"),
]