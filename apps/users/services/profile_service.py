from apps.users.dtos import GetProfileResponse
from apps.users.exceptions import UserNotFoundException
from apps.users.models import User

class ProfileService:
    
    @staticmethod
    def get_profile(account_id: str) -> GetProfileResponse:
        user = User.objects.get_by_account_id(account_id)

        if user is None:
            raise UserNotFoundException()
        
        return GetProfileResponse.model_validate(user)