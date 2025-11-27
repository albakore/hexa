from typing import BinaryIO
import asyncio
import boto3
from functools import partial
from modules.file_storage.application.exceptions import (
	FileStorageUploadException,
	FileStorageDownloadException,
)
from modules.file_storage.domain.repository.file_storage import FileStorageRepository
from botocore.exceptions import ClientError


class S3FileStorage(FileStorageRepository):
	def __init__(
		self,
		bucket_name: str,
		region: str,
		access_key: str,
		secret_key: str,
	):
		self.bucket_name = bucket_name
		self._session = boto3.Session(
			aws_access_key_id=access_key,
			aws_secret_access_key=secret_key,
			region_name=region,
		)
		self._s3 = self._session.client("s3")
		self._region = region

	async def upload_file(self, file: BinaryIO, filename: str) -> str:
		"""
		Sube un archivo a S3 usando boto3 en un thread pool para no bloquear el event loop.
		"""
		try:
			# Leer el contenido del archivo
			file_content = file.read()

			# Ejecutar la operación bloqueante en un thread pool
			loop = asyncio.get_event_loop()
			await loop.run_in_executor(
				None,
				partial(
					self._s3.put_object,
					Bucket=self.bucket_name,
					Key=filename,
					Body=file_content
				)
			)
		except ClientError as e:
			raise FileStorageUploadException(message=e)

		return (
			f"https://{self.bucket_name}.s3."
			f"{self._region}.amazonaws.com/{filename}"
		)

	async def download_file(self, filename: str) -> bytes:
		"""
		Descarga un archivo de S3 usando boto3 en un thread pool para no bloquear el event loop.
		"""
		try:
			# Ejecutar la operación bloqueante en un thread pool
			loop = asyncio.get_event_loop()
			response = await loop.run_in_executor(
				None,
				partial(
					self._s3.get_object,
					Bucket=self.bucket_name,
					Key=filename
				)
			)

			# Leer el body (esto también es bloqueante, así que lo ejecutamos en el executor)
			body = response["Body"]
			file_content = await loop.run_in_executor(None, body.read)
			return file_content
		except ClientError as e:
			raise FileStorageDownloadException(message=e)
