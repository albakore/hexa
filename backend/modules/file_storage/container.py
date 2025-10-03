from dependency_injector.containers import DeclarativeContainer

from dependency_injector.providers import Singleton, Factory, Configuration

from .adapter.output.file_metadata_adapter import FileMetadataAdapter
from .adapter.output.file_storage_adapter import FileStorageAdapter
from .adapter.output.s3_file_storage import S3FileStorage

from core.config.settings import env, Settings
from .adapter.output.sqlalchemy_file_metadata_storage import (
	FileMetadataSQLAlchemyRepository,
)
from modules.file_storage.application.service.file_storage import FileStorageService


class FileStorageContainer(DeclarativeContainer):
	config = Configuration(pydantic_settings=[env])

	s3_storage_repo = Singleton(
		S3FileStorage,
		bucket_name=config.AWS_ACCESS_BUCKET_NAME,
		region=config.AWS_ACCESS_REGION,
		access_key=config.AWS_ACCESS_KEY,
		secret_key=config.AWS_ACCESS_SECRET_KEY,
	)

	metadata_repo = Singleton(FileMetadataSQLAlchemyRepository)

	file_storage_adapter = Factory(
		FileStorageAdapter, file_storage_repository=s3_storage_repo
	)

	file_metadata_adapter = Factory(
		FileMetadataAdapter, file_metadata_repository=metadata_repo
	)

	service = Factory(
		FileStorageService,
		file_storage_repository=file_storage_adapter,
		file_metadata_repository=file_metadata_adapter,
	)
