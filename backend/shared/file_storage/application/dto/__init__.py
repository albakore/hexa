from dataclasses import dataclass

from shared.file_storage.domain.entity import FileMetadata


@dataclass
class FileStorageDTO:
	file: bytes
	metadata: FileMetadata
