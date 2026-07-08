from django.contrib.auth.base_user import BaseUserManager

from apps.accounts.enums import Role

class AccountManager(BaseUserManager):
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
