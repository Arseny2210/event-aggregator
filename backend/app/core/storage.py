"""Storage abstraction for uploaded files.

Provides an abstract StorageBackend interface and a LocalStorageBackend
implementation. ImportService depends on the abstraction, enabling future
swap to S3, Minio, or other backends without changing business logic.
"""

from abc import ABC, abstractmethod
from pathlib import Path

from app.core.config import settings


class StorageBackend(ABC):
    """Abstract interface for file storage operations."""

    @abstractmethod
    async def save(self, key: str, content: bytes) -> Path: ...

    @abstractmethod
    async def read(self, key: str) -> bytes: ...

    @abstractmethod
    async def delete(self, key: str) -> None: ...


class LocalStorageBackend(StorageBackend):
    """Stores files on the local filesystem under a configurable base directory."""

    def __init__(self, base_dir: Path | None = None) -> None:
        self.base_dir = base_dir or Path(settings.upload_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    async def save(self, key: str, content: bytes) -> Path:
        file_path = self.base_dir / key
        file_path.write_bytes(content)
        return file_path

    async def read(self, key: str) -> bytes:
        file_path = self.base_dir / key
        return file_path.read_bytes()

    async def delete(self, key: str) -> None:
        file_path = self.base_dir / key
        if file_path.exists():
            file_path.unlink()
