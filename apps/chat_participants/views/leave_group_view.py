from uuid import UUID

from shared.base_api_view import BaseApiView
from apps.chat_participants.member_service import MemberService

class LeaveGroupView(BaseApiView):
    def post(self, request, chat_id: UUID):
        """Handle member leave group request"""
        MemberService.leave(
            chat_id=chat_id,
            current_member_id=self.current_user,
        )

        return self.success_respone(
            message="Left the group successfully.",
        )