from shared.base_api_view import BaseApiView
from apps.chats.services import PrivateChatService
from apps.chats.dtos import CreatePrivateChatRequest
from apps.chats.serializers import CreatePrivateChatSerializer

class PrivateChatView(BaseApiView):
    """
    View for private chat
    Private endpoint (Authentication required)
    """
    def post(self, request):
        """Create or get a private chat"""
        serializer = CreatePrivateChatSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        dto = CreatePrivateChatRequest.model_validate(serializer.validated_data)

        result = PrivateChatService.get_or_create(
            current_user=self.current_user,
            dto=dto,
        )

        return self.success_respone(
            message="Private chat opened successfully.",
            data=result.model_dump(mode="json"),
        )