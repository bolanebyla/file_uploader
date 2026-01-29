from collections.abc import AsyncIterator
from dataclasses import dataclass
from pathlib import Path

import aiofiles


@dataclass(kw_only=True, slots=True)
class FileStreaming:
    media_type: str
    content: AsyncIterator[bytes]


class DownloadFileService:
    def __init__(
        self,
        files_dir: Path,
        chunk_size_bytes: int = 1024,
    ):
        self._files_dir = files_dir
        self._chunk_size_bytes = chunk_size_bytes

    async def get_file_streaming(self, short_file_path: Path) -> FileStreaming:
        return FileStreaming(
            media_type="image/jpeg",  # TODO: брать из meta файла
            content=self.get_file_stream(short_file_path=short_file_path),
        )

    async def get_file_stream(self, short_file_path: Path) -> AsyncIterator[bytes]:
        full_file_path = self.get_full_file_path(short_file_path=short_file_path)

        async with aiofiles.open(full_file_path, "rb") as file:
            while True:
                chunk = await file.read(self._chunk_size_bytes)

                if not chunk:
                    break

                yield chunk

    def get_full_file_path(self, short_file_path: Path) -> Path:
        return self._files_dir / short_file_path
