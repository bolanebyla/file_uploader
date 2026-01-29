from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile
from starlette.responses import StreamingResponse

from file_uploader.http_api.deps import create_download_file_service, create_upload_file_service
from file_uploader.services import DownloadFileService, UploadFileService

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


@upload_files_router.get("/download_file")
async def download_file(
    download_file_service: Annotated[DownloadFileService, Depends(create_download_file_service)],
    short_file_path: str,
) -> StreamingResponse:
    """Скачивание файла"""
    file_streaming = await download_file_service.get_file_streaming(
        short_file_path=Path(short_file_path),
    )
    return StreamingResponse(file_streaming.content, media_type=file_streaming.media_type)
