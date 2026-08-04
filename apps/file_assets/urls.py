from django.urls import path
from apps.file_assets.views import FileUploadView

urlpatterns = [
    path("", FileUploadView.as_view(), name="upload-file"),
]