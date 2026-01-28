from pathlib import Path
from typing import Annotated

from fastapi import Depends, Request

from file_uploader.http_api.settings import HttpApiSettings
from file_uploader.services import UploadFileService


def get_api_settings(request: Request) -> HttpApiSettings:
    return request.app.state.api_settings


def create_upload_file_service(
    api_settings: Annotated[HttpApiSettings, Depends(get_api_settings)],
) -> UploadFileService:
    return UploadFileService(files_dir=Path(api_settings.FILES_DIR))
