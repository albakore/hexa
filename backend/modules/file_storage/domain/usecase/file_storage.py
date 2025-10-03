from dataclasses import dataclass
from typing import BinaryIO

from modules.file_storage.domain.repository.file_storage import FileStorageRepository


@dataclass
class UploadFileToStorageUseCase:
	file_storage_repository: FileStorageRepository

	async def __call__(self, file: BinaryIO, filename: str) -> str:
		return await self.file_storage_repository.upload_file(file, filename)


@dataclass
class DownloadFileFromStorageUseCase:
	file_storage_repository: FileStorageRepository

	async def __call__(self, filename: str) -> bytes:
		return await self.file_storage_repository.download_file(filename)


@dataclass
class FileStorageUseCaseFactory:
	file_storage_repository: FileStorageRepository

	def __post_init__(self):
		self.upload_file_to_storage = UploadFileToStorageUseCase(
			self.file_storage_repository
		)
		self.download_file_from_storage = DownloadFileFromStorageUseCase(
			self.file_storage_repository
		)
