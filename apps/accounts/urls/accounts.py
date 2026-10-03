from django.urls import path

from apps.accounts.views import AccountView, AccountDetailView

urlpatterns = [
    path("", AccountView.as_view(), name="account-list"),
    path("<uuid:account_id>", AccountDetailView.as_view(), name="account-detail"),
]