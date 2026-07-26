from http import HTTPStatus

from rest_framework.views import APIView
from django.utils.functional import cached_property
from rest_framework.response import Response
from rest_framework.request import Request

from .api_response import APIResponse

class BaseApiView(APIView):
    """Base API view for all authenticated endpoints"""
    @property
    def current_account(self):
        return self.request.user
    
    @cached_property
    def current_user(self):
        return self.current_account.user_profile

    @staticmethod
    def success_respone(
        *,
        message: str | None = None,
        data=None,
        http_status: HTTPStatus = HTTPStatus.OK
    ):
        return Response(
            APIResponse.success(
                message=message,
                data=data,
            ),
            status=http_status,
        )