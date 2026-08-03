from django.conf import settings

from .protocols import StorageProtocol
from .local import LocalStorage

def get_storage() -> StorageProtocol:

    backend = settings.STORAGE_BACKEND

    if backend == "local":
        return LocalStorage()