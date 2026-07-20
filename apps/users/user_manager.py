from django.db import models

class UserManager(models.Manager):
    """Manager for User model"""
    
    def get_by_account_id(self, account_id):
        """Get user information by id"""
        return self.filter(account_id=account_id).first()
    
    def get_by_id(self, user_id):
        """Get user by id"""
        return self.filter(id=user_id).first()
    
    def get_active_users(self):
        """Get all active users"""
        return (
            self.select_related("account")
            .filter(account__is_active=True)
        )
    
    def get_active_users_by_ids(self, user_ids):
        return (
            self.get_active_users()
            .filter(id__in=user_ids)
        )

    def update_profile(self, user, **fields):
        """Update user profile information"""
        for field, value in fields.items():
            setattr(user, field, value)

        user.save(update_fields=[*fields.keys(), "updated_at"])
        return user

    def search_active_users(self, q):
        """Get all active user for search"""
        queryset = self.get_active_users()

        if q:
            queryset = queryset.filter(
                full_name__icontains=q
            )

        return queryset.order_by("-created_at")