from uuid import UUID

from shared.base_api_view import BaseApiView
from apps.chat_participants.member_service import MemberService

class DeleteGroupMemberView(BaseApiView):
    def delete(self, request, chat_id: UUID, member_id: UUID):
        """
        Handle delete member from group request
        """
        MemberService.delete_member(
            chat_id=chat_id,
            current_user_id=self.current_user,
            member_id=member_id,
        )

        return self.success_respone(
            message="Member removed successfully."
        )