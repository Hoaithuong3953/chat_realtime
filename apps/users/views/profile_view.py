from apps.users.services import ProfileService
from apps.users.dtos import UpdateProfileRequest
from apps.users.serializers import UpdateProfileSerializer
from shared.base_api_view import BaseApiView

class ProfileView(BaseApiView):
    
    def get(self, request):
        """Handle get user information request"""
        result = ProfileService.get_profile(account_id=request.user.id)

        return self.success_respone(
            message="Get profile successfully.",
            data=result.model_dump(mode="json")
        )
    
    def patch(self, request):
        """Handle update user information request"""
        serializer = UpdateProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        dto = UpdateProfileRequest.model_validate(serializer.validated_data)
        
        result = ProfileService.update_profile(
            account_id=request.user.id,
            dto=dto,
        )

        return self.success_respone(
            message="Profile updated successfully.",
            data=result.model_dump(mode="json")
        )