from pathlib import Path
from uuid import UUID, uuid4
from django.core.files.uploadedfile import UploadedFile
from django.utils import timezone

from apps.file_assets.constants import MAX_UPLOAD_FILE_SIZE, ALLOWED_FILE_TYPES
from core.storage.factory import get_storage
from shared.exceptions.chat.file import (
    FileAccessDeniedException,
    FileNotReadyException,
    FileTooLargeException,
    EmptyFileException,
    FileNotFoundException,
    FileUploadFailedException,
    InvalidContentTypeException,
    InvalidFileExtensionException,
    FileStorageNotFoundException,
)
from apps.file_assets.models import FileAsset
from apps.file_assets.dtos import UploadFileResponse
from apps.file_assets.enums import FileStatus
from core.storage.protocols import StorageProtocol

class FileService:
    @staticmethod
    def _validate_file(file: UploadedFile | None) -> None:
        """
        Validate the uploaded file

        Args:
            file: The uploaded file to validate

        Raises:
            FileNotFoundException: if no file is provided
            EmptyFileException: if the file is empty
            FileTooLargeException: if the file size exceeds the maximum allowed limit
            InvalidFileExtensionException: if the file extension is not supported
            InvalidContentTypeException: if the file content type does not match the expected type
        """
        # Check if file is not exist
        if file is None:
            raise FileNotFoundException()

        # Check if file is empty
        if file.size <= 0:
            raise EmptyFileException()

        # Check if the file size is too large
        if file.size > MAX_UPLOAD_FILE_SIZE:
            raise FileTooLargeException(f"{MAX_UPLOAD_FILE_SIZE} MB")

        extension = Path(file.name).suffix.lower()
        expected_content_type = ALLOWED_FILE_TYPES.get(extension)

        # Check if the content type is empty
        if expected_content_type is None:
            raise InvalidFileExtensionException()

        # Check if the content type is not supported
        if file.content_type != expected_content_type:
            raise InvalidContentTypeException()

    @staticmethod
    def validate_uploaded_file(
        file_ids: list[UUID],
        user_id: UUID,
    ) -> list[FileAsset]:
        files = FileAsset.objects.get_active_by_ids(file_ids)
        storage = get_storage()
        
        if len(files) != len(file_ids):
            raise FileNotFoundException()

        for file in files:

            if file.status != FileStatus.UPLOADED:
                raise FileNotReadyException()

            if file.user_id != user_id:
                raise FileAccessDeniedException()

            if not storage.exist(file.storage_key):
                raise FileStorageNotFoundException()

        return files

    @staticmethod
    def _generate_storage_key(original_name: str) -> str:
        """Generate a unique storage key for an uploaded file"""
        extension = Path(original_name).suffix.lower()

        today = timezone.now()

        return (
            f"uploads/"
            f"{today:%Y}/"
            f"{today:%m}/"
            f"{uuid4()}{extension}"
        )

    @staticmethod
    def upload(file: UploadedFile, user_id: UUID, storage: StorageProtocol) -> UploadFileResponse:
        """Upload a file to the configured storage"""
        FileService._validate_file(file=file)

        storage_key = FileService._generate_storage_key(file.name)

        file_asset = FileAsset.objects.create_file(
            user_id=user_id,
            storage_key=storage_key,
            original_name=file.name,
            content_type=file.content_type,
            file_size=file.size,
            status=FileStatus.PENDING,
        )

        try:
            storage_key = storage.upload(
                file=file,
                path=storage_key,
            )
        except Exception:
            FileAsset.objects.update_status(file_asset.id, FileStatus.FAILED)

            storage.delete(storage_key)
            raise FileUploadFailedException()

        FileAsset.objects.update_status(file_asset.id, FileStatus.UPLOADED)
        
        file_asset.refresh_from_db()

        return UploadFileResponse.model_validate(file_asset)