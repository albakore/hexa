from typing import BinaryIO

from modules.file_storage.domain.repository.file_storage import FileStorageRepository


class FileStorageAdapter(FileStorageRepository):
	def __init__(self, file_storage_repository: FileStorageRepository):
		self.file_storage_repository = file_storage_repository

	async def upload_file(self, file: BinaryIO, filename: str) -> str:
		return await self.file_storage_repository.upload_file(file, filename)

	async def download_file(self, filename: str) -> bytes:
		return await self.file_storage_repository.download_file(filename)
