from abc import ABC, abstractmethod
from typing import BinaryIO


class FileStorageRepository(ABC):
	@abstractmethod
	async def upload_file(
		self, file: BinaryIO, filename: str, content_type: str
	) -> str:  # URL
		...

	@abstractmethod
	async def download_file(self, filename: str) -> bytes:  # contenido crudo
		...
