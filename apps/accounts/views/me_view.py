from rest_framework.views import APIView
from rest_framework.response import Response
from http import HTTPStatus

from apps.accounts.services.me_service import MeService
from shared.responses import APIResponse

class MeView(APIView):

    def get(self, request):
        result = MeService.me(account_id=request.user.id)

        return Response(
            APIResponse.success(
                message="Get current user successfully.",
                data=result.model_dump(mode="json")
            ),
            status=HTTPStatus.OK
        )