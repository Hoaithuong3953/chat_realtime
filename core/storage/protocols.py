from typing import Protocol
from django.core.files.uploadedfile import UploadedFile

class StorageProtocol(Protocol):

    def upload(self, path: str, file: UploadedFile) -> str:
        """Save file and return storage path"""
        ...

    def delete(self, path: str) -> None:
        """Delete file"""
        ...

    def exist(self, path: str) -> bool:
        """Check if physical file is exist"""
        ...