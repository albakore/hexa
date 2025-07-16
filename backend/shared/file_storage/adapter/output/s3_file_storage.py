from typing import BinaryIO
import boto3
from shared.file_storage.domain.repository.file_storage import FileStorageRepository


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
			region_name=region
			)
		self._s3 = self._session.client("s3")
		self._bucket_name = bucket_name

	async def upload_file(
		self, file: BinaryIO, filename: str
	) -> str:
		self._s3.upload_fileobj(
			Fileobj=file,
			Bucket=self.bucket_name,
			Key=filename
		)
		return (
			f"https://{self.bucket_name}.s3."
			f"{self._s3.meta.region_name}.amazonaws.com/{filename}"
		)
	
	async def download_file(self, filename: str) -> dict:
		response = self._s3.get_object(
			Bucket=self.bucket_name,
			Key=filename,
		)
		return response
