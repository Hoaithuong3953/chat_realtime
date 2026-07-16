from rest_framework.views import APIView
from rest_framework.response import Response
from http import HTTPStatus

from apps.users.services import ProfileService
from apps.users.dtos import UpdateProfileRequest
from apps.users.serializers import UpdateProfileSerializer
from shared.api_response import APIResponse

class ProfileView(APIView):
    
    def get(self, request):
        result = ProfileService.get_profile(account_id=request.user.id)

        return Response(
            APIResponse.success(
                message="Get profile successfully.",
                data=result.model_dump(mode="json")
            ),
            status=HTTPStatus.OK
        )
    
    def patch(self, request):
        serializer = UpdateProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        dto = UpdateProfileRequest.model_validate(serializer.validated_data)
        
        result = ProfileService.update_profile(
            account_id=request.user.id,
            dto=dto,
        )

        return Response(
            APIResponse.success(
                message="Profile updated successfully.",
                data=result.model_dump(mode="json")
            ),
            status=HTTPStatus.OK,
        )