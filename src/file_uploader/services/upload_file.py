import asyncio
import logging
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

import aiofiles
from fastapi import UploadFile


@dataclass
class UploadedFileDownloadUrls:
    original_file_url: str
    new_file_url: str


class UploadFileService:
    """
    Сервис для загрузки файла
    """

    def __init__(
        self,
        files_dir: Path,
        chunk_size_bytes: int = 1024,
        original_file_prefix: str = "",
        new_file_prefix: str = "new_",
    ):
        self._files_dir = files_dir
        self._chunk_size_bytes = chunk_size_bytes
        self._original_file_prefix = original_file_prefix
        self._new_file_prefix = new_file_prefix

        self._logger = logging.getLogger(self.__class__.__name__)

    async def upload_file(self, file: UploadFile):
        parend_dir_name = self._create_parend_dir_name()
        file_id = self._create_file_id()

        file_path = self._create_file_path(
            parend_dir_name=parend_dir_name,
            file_id=file_id,
        )
        await self._create_file_dir(file_path=file_path)

        original_file_name = f"{self._original_file_prefix}{file.filename}"
        new_file_name = f"{self._new_file_prefix}{file.filename}"

        async with (
            aiofiles.open(file_path / original_file_name, "wb") as original_file,
            aiofiles.open(file_path / new_file_name, "wb") as new_file,
        ):
            while True:
                line = await file.read(self._chunk_size_bytes)
                if not line:
                    break

                await original_file.write(line)
                await new_file.write(line)

        return UploadedFileDownloadUrls(
            original_file_url=f"{parend_dir_name}/{file_id}/{original_file_name}",
            new_file_url=f"{parend_dir_name}/{file_id}/{new_file_name}",
        )

    def _create_file_id(self) -> str:
        return str(uuid4())

    def _create_parend_dir_name(self) -> str:
        today = datetime.now(tz=UTC).date()
        return today.isoformat()

    def _create_file_path(self, parend_dir_name: str, file_id: str) -> Path:
        file_path = self._files_dir / parend_dir_name / file_id
        return file_path

    async def _create_file_dir(self, file_path: Path) -> None:
        await asyncio.to_thread(file_path.mkdir, parents=True, exist_ok=True)
