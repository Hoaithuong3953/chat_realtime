from django.contrib.auth.base_user import BaseUserManager

from apps.users.enums import UserRole

class UserManager(BaseUserManager):
    """Custom manager for User model"""

    def create_user(self, email: str, username: str, password: str, name: str, **extra_fields):
        """Create and return a regular user"""        
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", UserRole.USER)

        user = self.model(
            email=email,
            username=username,
            name=name,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email: str, username: str, password: str, name: str, **extra_fields):
        """Create and return a super user"""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", UserRole.ADMIN)

        if not extra_fields.get("is_staff"):
            raise ValueError("Superuser must have is_staff=True")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(email, username, password, name, **extra_fields)
    
    def email_exists(self, email: str) -> bool:
        """Check if email already exists"""
        return self.filter(email=email).exists()

    def username_exists(self, username: str) -> bool:
        """Check if username already exists"""
        return self.filter(username=username).exists()