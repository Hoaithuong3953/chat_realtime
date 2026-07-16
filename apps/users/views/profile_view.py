from rest_framework.views import APIView
from rest_framework.response import Response
from http import HTTPStatus

from apps.users.services import ProfileService
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