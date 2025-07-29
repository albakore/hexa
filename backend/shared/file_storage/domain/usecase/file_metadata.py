from dataclasses import dataclass
import uuid

from core.db import Transactional
from shared.file_storage.domain.command import CreateFileMetadataCommand
from shared.file_storage.domain.entity.file_metadata import FileMetadata
from shared.file_storage.domain.exception import FileMetadataNotFoundException
from shared.file_storage.domain.repository.file_metadata import FileMetadataRepository


@dataclass
class GetFileMetadataByUuidUseCase:
	file_metadata_repository : FileMetadataRepository

	async def __call__(self, uuid: uuid.UUID) -> FileMetadata | None:
		file_metadata = await self.file_metadata_repository.get_by_uuid(uuid)
		if not file_metadata:
			raise FileMetadataNotFoundException
		return file_metadata

@dataclass
class CreateFileMetadataUseCase:
	file_metadata_repository : FileMetadataRepository

	def __call__(self,command : CreateFileMetadataCommand) -> FileMetadata: 
		return FileMetadata.model_validate(command)

@dataclass
class SaveFileMetadataUseCase:
	file_metadata_repository : FileMetadataRepository

	@Transactional()
	async def __call__(self,file_metadata: FileMetadata) -> None:
		return await self.file_metadata_repository.save(file_metadata)

@dataclass
class DeleteFileMetadataUseCase:
	file_metadata_repository : FileMetadataRepository

	@Transactional()
	async def __call__(self,file_metadata: FileMetadata) -> None:
		return await self.file_metadata_repository.delete(file_metadata)


@dataclass
class FileMetadataUseCaseFactory:
	file_metadata_repository : FileMetadataRepository

	def __post_init__(self):
		self.get_file_metadata_by_uuid = GetFileMetadataByUuidUseCase(
			self.file_metadata_repository
		)
		self.create_file_metadata = CreateFileMetadataUseCase(
			self.file_metadata_repository
		)
		self.save_file_metadata = SaveFileMetadataUseCase(
			self.file_metadata_repository
		)
		self.delete_file_metadata = DeleteFileMetadataUseCase(
			self.file_metadata_repository
		)