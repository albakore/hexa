from dataclasses import dataclass

from modules.file_storage.domain.entity import FileMetadata


@dataclass
class FileStorageDTO:
	file: bytes
	metadata: FileMetadata
