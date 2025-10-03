from dataclasses import dataclass
from typing import BinaryIO
from uuid import UUID

from modules.file_storage.domain.command import CreateFileMetadataCommand
from modules.file_storage.domain.entity.file_metadata import FileMetadata
from modules.file_storage.domain.repository.file_metadata import FileMetadataRepository


class FileMetadataAdapter(FileMetadataRepository):
	def __init__(self, file_metadata_repository: FileMetadataRepository):
		self.file_metadata_repository = file_metadata_repository

	async def get_by_uuid(self, uuid: UUID) -> FileMetadata | None:
		return await self.file_metadata_repository.get_by_uuid(uuid)

	async def create(self, command: CreateFileMetadataCommand) -> FileMetadata:
		return await self.create(command)

	async def save(self, file_metadata: FileMetadata) -> None:
		return await self.file_metadata_repository.save(file_metadata)

	async def delete(self, file_metadata: FileMetadata) -> None:
		return await self.file_metadata_repository.delete(file_metadata)
