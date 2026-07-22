from uuid import UUID

from shared.base_api_view import BaseApiView
from apps.chat_participants.member_service import MemberService
from apps.chat_participants.serializers import AddMemberSerializer
from apps.chat_participants.dtos import AddGroupMembersRequest

class GroupMemberView(BaseApiView):
    def get(self, request, chat_id: UUID):
        """
        Handle group member listing request
        """
        result = MemberService.get_all(chat_id=chat_id, user_id=self.current_user)

        return self.success_respone(
            message="Group members retrieved successfully.",
            data=result.model_dump(mode="json"),
        )

    def post(self, request, chat_id: UUID):
        """
        Handle add group member request
        """
        serializer = AddMemberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        dto = AddGroupMembersRequest.model_validate(serializer.validated_data)

        result = MemberService.add_member(
            chat_id=chat_id,
            user_id=self.current_user,
            dto=dto,
        )

        return self.success_respone(
            message="Members added successfully.",
            data=result.model_dump(mode="json"),
        )