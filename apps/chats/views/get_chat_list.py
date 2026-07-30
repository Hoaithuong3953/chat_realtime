from shared.base_api_view import BaseApiView
from apps.chats.dtos import GetChatListRequest
from apps.chats.serializers import GetChatListSerializer
from apps.chats.services import ChatListService

class GetChatListView(BaseApiView):

    def get(self, request):
        serializer = GetChatListSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        dto = GetChatListRequest.model_validate(serializer.validated_data)

        result = ChatListService.get(
            user_id=self.current_user.id,
            dto=dto,
        )

        return self.success_respone(
            message="Get chat list successfully.",
            data=result.model_dump(mode="json"),
        )