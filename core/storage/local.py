from django.core.files.uploadedfile import UploadedFile
from django.core.files.storage import default_storage

from .protocols import StorageProtocol

class LocalStorage(StorageProtocol):
    def upload(self, path: str, file: UploadedFile) -> str:
        
        saved_path = default_storage.save(
            path,
            file,
        )
        return saved_path

    def delete(self, path: str) -> None:
        default_storage.delete(path)