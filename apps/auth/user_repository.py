from apps.auth.models import User

class UserRepository:
    """
    Repository class for User model

    Methods:
    - exists_by_email: Check if a user exists by email
    - exists_by_username: Check if a user exists by username
    - create_user: Create a new user
    """
    @staticmethod
    def exists_by_email(email: str) -> bool:
        return User.objects.filter(email=email).exists()
    
    @staticmethod
    def exists_by_username(username: str) -> bool:
        return User.objects.filter(username=username).exists()
    
    @staticmethod
    def create_user(**kwargs) -> User:
        return User.objects.create(**kwargs)