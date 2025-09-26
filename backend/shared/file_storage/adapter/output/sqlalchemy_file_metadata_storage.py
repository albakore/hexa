from uuid import UUID
from core.db import session, session_factory
from shared.file_storage.domain.command import CreateFileMetadataCommand
from shared.file_storage.domain.entity.file_metadata import FileMetadata
from shared.file_storage.domain.repository.file_metadata import FileMetadataRepository


class FileMetadataSQLAlchemyRepository(FileMetadataRepository):
	async def get_by_uuid(self, uuid: UUID) -> FileMetadata | None:
		async with session_factory() as session:
			file_metadata = await session.get(FileMetadata, uuid)
		return file_metadata

	def create(self, command: CreateFileMetadataCommand) -> FileMetadata:
		return FileMetadata.model_validate(command)

	async def save(self, file_metadata: FileMetadata) -> None:
		session.add(file_metadata)
		await session.flush()

	async def delete(self, file_metadata: FileMetadata) -> None:
		await session.delete(file_metadata)
