from django.contrib.auth.base_user import BaseUserManager
from django.db.models import Q

class UserManager(BaseUserManager):
    """Custom manager for User model"""

    def get_by_email(self, email: str):
        """Get user by email"""
        return self.filter(email=email).first()
    
    def get_by_username(self, username: str):
        """Get user by username"""
        return self.filter(username=username).first()
    
    def get_by_identify(self, identifier: str):
        """Get user by username or email"""
        return self.filter(
            Q(email=identifier) | Q(username=identifier)
        ).first()