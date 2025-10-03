from abc import ABC, abstractmethod
from typing import BinaryIO
import uuid

from modules.file_storage.domain.command import CreateFileMetadataCommand
from modules.file_storage.domain.entity.file_metadata import FileMetadata


class FileMetadataRepository(ABC):
	@abstractmethod
	async def get_by_uuid(self, uuid: uuid.UUID) -> FileMetadata | None: ...

	@abstractmethod
	def create(self, command: CreateFileMetadataCommand) -> FileMetadata: ...

	@abstractmethod
	async def save(self, file_metadata: FileMetadata) -> None: ...

	@abstractmethod
	async def delete(self, file_metadata: FileMetadata) -> None: ...
