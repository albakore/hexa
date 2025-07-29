
from dataclasses import dataclass
from datetime import datetime
import pathlib
import uuid
from shared.file_storage.domain.command import CreateFileMetadataCommand, SaveFileCommand
from shared.file_storage.domain.repository.file_metadata import FileMetadataRepository
from shared.file_storage.domain.repository.file_storage import FileStorageRepository
from shared.file_storage.domain.usecase.file_metadata import FileMetadataUseCaseFactory
from shared.file_storage.domain.usecase.file_storage import FileStorageUseCaseFactory


@dataclass
class FileStorageService:
	file_storage_repository : FileStorageRepository
	file_metadata_repository : FileMetadataRepository

	def __post_init__(self):
		self.storage_usecase = FileStorageUseCaseFactory(self.file_storage_repository)
		self.metadata_usecase = FileMetadataUseCaseFactory(self.file_metadata_repository)
	
	async def save_file(self, command: SaveFileCommand):
		uuid_for_file = uuid.uuid4()
		today = datetime.now()
		file_path = f"{today.year}{command.path_target}/{command.filename}"
		if not command.path_target:
			file_extension = pathlib.Path(command.filename).suffix
			file_path = f"{today.year}/{today.month}/{today.day}/{uuid_for_file}{file_extension}"

		await self.storage_usecase.upload_file_to_storage(
			file=command.file,
			filename=file_path
		)

		file_metadata_command = CreateFileMetadataCommand()


