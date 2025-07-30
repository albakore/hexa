from dataclasses import dataclass
from datetime import datetime
import pathlib
import uuid

from shared.file_storage.application.dto import FileStorageDTO
from shared.file_storage.domain.command import (
	CreateFileMetadataCommand,
	SaveFileCommand,
)
from shared.file_storage.domain.entity import FileMetadata
from shared.file_storage.domain.exception import FileMetadataNotFoundException
from shared.file_storage.domain.repository.file_metadata import FileMetadataRepository
from shared.file_storage.domain.repository.file_storage import FileStorageRepository
from shared.file_storage.domain.usecase.file_metadata import FileMetadataUseCaseFactory
from shared.file_storage.domain.usecase.file_storage import FileStorageUseCaseFactory


@dataclass
class FileStorageService:
	file_storage_repository: FileStorageRepository
	file_metadata_repository: FileMetadataRepository

	def __post_init__(self):
		self.storage_usecase = FileStorageUseCaseFactory(self.file_storage_repository)
		self.metadata_usecase = FileMetadataUseCaseFactory(
			self.file_metadata_repository
		)

	async def save_file(self, command: SaveFileCommand):
		uuid_for_file = uuid.uuid4()
		today = datetime.now()
		file_extension = pathlib.Path(command.filename).suffix
		filename = str(uuid_for_file) + file_extension
		file_path = f"{today.year}/{today.month}/{today.day}/{filename}"
		if command.path_target:
			file_path = f"{today.year}{command.path_target}/{filename}"

		await self.storage_usecase.upload_file_to_storage(
			file=command.file,
			filename=file_path,
		)

		file_metadata_command = CreateFileMetadataCommand(
			id=uuid_for_file,
			path_target=file_path,
			filename=filename,
			download_filename=command.filename,
			size=command.size
		)

		file_metadata = self.metadata_usecase.create_file_metadata(
			file_metadata_command
		)

		return await self.metadata_usecase.save_file_metadata(file_metadata)
	
	async def download_file(self, file_metadata_uuid: uuid.UUID):
		metadata = await self.metadata_usecase.get_file_metadata_by_uuid(file_metadata_uuid)
		file = await self.storage_usecase.download_file_from_storage(metadata.path_target or metadata.filename)
		return FileStorageDTO(file,metadata)

	async def get_metadata(self, file_metadata_uuid: uuid.UUID) -> FileMetadata:
		return await self.metadata_usecase.get_file_metadata_by_uuid(file_metadata_uuid)
		