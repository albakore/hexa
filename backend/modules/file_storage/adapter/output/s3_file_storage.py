from typing import BinaryIO, cast
import boto3
from modules.file_storage.application.exceptions import (
	FileStorageUploadException,
	FileStorageDownloadException,
)
from modules.file_storage.domain.repository.file_storage import FileStorageRepository
from botocore.exceptions import ClientError
from botocore.response import StreamingBody


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
		self._bucket_name = bucket_name

	async def upload_file(self, file: BinaryIO, filename: str) -> str:
		try:
			self._s3.upload_fileobj(Fileobj=file, Bucket=self.bucket_name, Key=filename)
		except ClientError as e:
			raise FileStorageUploadException(message=e)

		return (
			f"https://{self.bucket_name}.s3."
			f"{self._s3.meta.region_name}.amazonaws.com/{filename}"
		)

	async def download_file(self, filename: str) -> bytes:
		try:
			response = self._s3.get_object(
				Bucket=self.bucket_name,
				Key=filename,
			)
			body = cast(StreamingBody, response["Body"])
			return body.read()
		except ClientError as e:
			raise FileStorageDownloadException(message=e)
