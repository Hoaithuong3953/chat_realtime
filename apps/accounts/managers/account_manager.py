from __future__ import annotations
from typing import TYPE_CHECKING
from uuid import UUID
from django.contrib.auth.base_user import BaseUserManager
from django.db.models import Q
from django.utils import timezone


from apps.accounts.enums import Role

if TYPE_CHECKING:
    from apps.accounts.models import Account

class AccountManager(BaseUserManager["Account"]):
    """
    Manager for Account model

    Provides helper methods for authentication and authorization
    """
    def create_account(self, email: str, username: str, password: str, **extra_fields):
        """Create and return a regular user account"""
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", Role.USER)

        account = self.model(
            email=email,
            username=username,
            **extra_fields,
        )

        account.set_password(password)
        account.save(using=self._db)

        return account

    def email_exists(self, email: str) -> bool:
        """Check if email already exists"""
        return self.filter(email=email).exists()

    def username_exists(self, username: str) -> bool:
        """Check if username already exists"""
        return self.filter(username=username).exists()
    
    def get_by_identifier(self, identifier: str):
        """Get user by username or email"""
        return self.filter(
            Q(email=identifier) | Q(username=identifier)
        ).first()
    
    def get_by_id(self, account_id):
        """Get account by id"""
        return self.filter(id=account_id).first()

    def search_accounts(
        self,
        q: str | None = None,
        role: Role | None = None,
        is_active: bool | None = None,
    ):
        queryset = self.select_related("user_profile")

        if q:
            queryset = queryset.filter(
                Q(email__icontains=q)
                | Q(username__icontains=q)
                | Q(user_profile__full_name__icontains=q)
            )

        if role is not None:
            queryset = queryset.filter(role=role)

        if is_active is not None:
            queryset = queryset.filter(is_active=is_active)

        return queryset.order_by("-created_at")