from uuid import UUID
from django.db import transaction

from apps.chat_messages.dtos import (
    MessageResponse,
    SendDocumentMessageRequest,
    DocumentResponse,
    SendDocumentMessageResponse
)
from apps.chat_messages.dtos.send_documents_dto import MessageResponse
from apps.chat_messages.models.document_message_model import DocumentMessage
from apps.chat_messages.enums import MessageType
from apps.file_assets.models import FileAsset
from apps.file_assets.file_service import FileService
from .message_service import MessageService

class DocumentMessageService:

    @staticmethod
    def add_document_mesage(
        chat_id: UUID,
        user_id: UUID,
        dto: SendDocumentMessageRequest,
    ) -> SendDocumentMessageResponse:
        """
        Add document messages and optional text content to the chat
        """
        files = FileAsset.objects.get_active_by_ids(dto.file_ids)
        FileService.validate_uploaded_file(files, user_id)

        responses: list[MessageResponse] = []

        with transaction.atomic():
            if dto.text_content is not None:
                text = MessageService.create_message(
                    chat_id=chat_id,
                    user_id=user_id,
                    message_type=MessageType.TEXT,
                    text_content=dto.text_content,
                    reply_to_message=dto.reply_to_message,
                )
                responses.append(MessageResponse(
                    id=text.id,
                    chat=text.chat_id,
                    user=text.user_id,
                    message_type=text.message_type,
                    text_content=text.text_content,
                    reply_to_message=text.reply_to_message,
                    created_at=text.created_at,
                ))

            for file in files:
                document = MessageService.create_message(
                    chat_id=chat_id,
                    user_id=user_id,
                    text_content=None,
                    message_type=MessageType.DOCUMENT,
                    reply_to_message=dto.reply_to_message,
                )

                DocumentMessage.objects.create_document_message(
                    file_asset_id=file.id,
                    message_id=document.id,
                )

                responses.append(MessageResponse(
                    id=document.id,
                    chat=document.chat_id,
                    user=document.user_id,
                    message_type=document.message_type,
                    document=DocumentResponse(
                        file_asset_id=file.id,
                        original_name=file.original_name,
                        file_size=file.file_size,
                    ),
                    reply_to_message=document.reply_to_message,
                    created_at=document.created_at,
                ))

        return SendDocumentMessageResponse(messages=responses)