from django.db import models

class UserManager(models.Manager):
    """Manager for User model"""
    
    def get_by_account_id(self, account_id):
        """Get user information by id"""
        return self.filter(account_id=account_id).first()

    def update_profile(self, user, **fields):
        """Update user profile information"""
        for field, value in fields.items():
            setattr(user, field, value)

        user.save(update_fields=[*fields.keys(), "updated_at"])
        return user