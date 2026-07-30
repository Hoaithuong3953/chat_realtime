from apps.users.dtos import GetProfileResponse, UpdateProfileRequest, UpdateProfileResponse
from apps.users.exceptions import UserNotFoundException
from apps.users.models import User

class ProfileService:
    
    @staticmethod
    def get_profile(account_id: str) -> GetProfileResponse:
        user = User.objects.get_by_account_id(account_id)

        if user is None:
            raise UserNotFoundException()
        
        return GetProfileResponse.model_validate(user)
    
    @staticmethod
    def update_profile(account_id: str, dto: UpdateProfileRequest) -> UpdateProfileResponse:
        user = User.objects.get_by_account_id(account_id)

        if user is None:
            raise UserNotFoundException()
        
        data = dto.model_dump(exclude_unset=True)
        user = User.objects.update_profile(user, **data)
        
        return UpdateProfileResponse.model_validate(user)