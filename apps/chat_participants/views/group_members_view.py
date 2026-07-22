from uuid import UUID

from shared.base_api_view import BaseApiView
from apps.chat_participants.member_service import MemberService

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