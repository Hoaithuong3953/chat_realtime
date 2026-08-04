from shared.base_api_view import BaseApiView
from apps.file_assets.file_service import FileService
from core.storage.factory import get_storage

class FileUploadView(BaseApiView):

    def post(self, request):
        """Handle upload file and storage file request"""
        result = FileService.upload(
            file=request.FILES.get("file"),
            user_id=self.current_user.id,
            storage=get_storage(),
        )

        return self.success_respone(
            message="File upload successfully.",
            data=result.model_dump(mode="json"),
        )