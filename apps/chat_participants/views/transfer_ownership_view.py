from uuid import UUID

from shared.base_api_view import BaseApiView
from apps.chat_participants.dtos import TransferOwnershipRequest
from apps.chat_participants.serializers import TransferOwnershipSerializer
from apps.chat_participants.member_service import MemberService

class TransferOwnershipView(BaseApiView):

    def patch(self, request, chat_id: UUID):
        """Handle transfer ownership request"""
        serializer = TransferOwnershipSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        dto = TransferOwnershipRequest.model_validate(serializer.validated_data)

        result = MemberService.transfer_ownership(
            chat_id=chat_id,
            current_user_id=self.current_user,
            dto=dto,
        )

        return self.success_respone(
            message="Group ownership transferred successfully.",
            data=result,
        )