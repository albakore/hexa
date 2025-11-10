"""
Protocolo para servicios del módulo FileStorage.

Permite type checking y autocompletado sin crear dependencias directas
entre otros módulos.
"""

from typing import Any, Optional, Protocol, Self
from uuid import UUID


class FileStorageServiceProtocol(Protocol):
	"""
	API pública del módulo FileStorage.

	Expone operaciones para gestión de archivos en S3/storage.
	"""

	def __call__(self) -> Self: ...
	async def save_file(self, command: Any) -> Optional[Any]:
		"""
		Guarda un archivo en el storage.

		Args:
			command: SaveFileCommand con file, filename, size

		Returns:
			FileMetadata del archivo guardado

		Used by: provider (draft invoices)
		"""
		...

	async def download_file(self, file_metadata_uuid: UUID) -> Any:
		"""
		Descarga un archivo del storage.

		Returns:
			FileStorageDTO con (file: bytes, metadata: FileMetadata)

		Used by: provider (finalize invoice)
		"""
		...

	async def get_metadata(self, file_metadata_uuid: UUID) -> Any:
		"""
		Obtiene metadata de un archivo.

		Returns:
			FileMetadata

		Used by: provider (draft invoices)
		"""
		...
