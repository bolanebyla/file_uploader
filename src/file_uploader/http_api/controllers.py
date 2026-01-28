from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile

from file_uploader.http_api.deps import create_upload_file_service
from file_uploader.services import UploadFileService

upload_files_router = APIRouter(
    prefix="/files",
    tags=["Файлы"],
)


@upload_files_router.post("/upload_file")
async def upload_file(
    upload_file_service: Annotated[UploadFileService, Depends(create_upload_file_service)],
    file: UploadFile,
) -> None:
    """Загрузка файла"""
    return await upload_file_service.upload_file(file=file)
