from typing import BinaryIO
import boto3
from io import BytesIO
from botocore.client import Config
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
        self.client = boto3.client(
            "s3",
            region_name=region,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            config=Config(signature_version="s3v4"),
        )

    async def upload_file(
        self, file: BinaryIO, filename: str, content_type: str
    ) -> str:
        self.client.upload_fileobj(
            Fileobj=file,
            Bucket=self.bucket_name,
            Key=filename,
            ExtraArgs={"ContentType": content_type},
        )
        return (
            f"https://{self.bucket_name}.s3."
            f"{self.client.meta.region_name}.amazonaws.com/{filename}"
        )

    async def download_file(self, filename: str) -> bytes:
        buffer = BytesIO()
        self.client.download_fileobj(
            Bucket=self.bucket_name,
            Key=filename,
            Fileobj=buffer,
        )
        buffer.seek(0)
        return buffer.read()