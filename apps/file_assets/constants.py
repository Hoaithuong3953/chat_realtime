"""
Constants used by the file_assets module
"""

# Validation field file_asset model constants
STORAGE_KEY_MAX_LENGTH = 500
ORIGINAL_NAME_MAX_LENGTH = 255
CONTENT_TYPE_MAX_LENGTH = 100
STATUS_MAX_LENGTH = 20
REFERENCE_COUNT_DEFAULT = 0
MAX_UPLOAD_FILE_SIZE = 10 * 1024 * 1024

# Upload validation
DOCUMENT_TYPES = {
    ".pdf": "application/pdf",
    ".txt": "text/plain",
    ".doc": "application/msword",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".xls": "application/vnd.ms-excel",
    ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ".ppt": "application/vnd.ms-powerpoint",
    ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
}

IMAGE_TYPES = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".gif": "image/gif",
    ".webp": "image/webp",
}

VIDEO_TYPES = {
    ".mp4": "video/mp4",
    ".mov": "video/quicktime",
    ".avi": "video/x-msvideo",
    ".mkv": "video/x-matroska",
    ".webm": "video/webm",
}

ALLOWED_FILE_TYPES = {
    **DOCUMENT_TYPES,
    **IMAGE_TYPES,
    **VIDEO_TYPES,
}