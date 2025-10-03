from typing import BinaryIO
import pytest
from modules.file_storage.container import FileStorageContainer
from faker import Faker

faker = Faker()


@pytest.mark.asyncio
async def test_upload_file():
	repo = FileStorageContainer().s3_storage_repo()
	with open("shared/file_storage/test/string.pdf", "rb") as f:
		result = await repo.upload_file(f, f.name)
		print(result)


@pytest.mark.asyncio
async def test_download_file():
	repo = FileStorageContainer().s3_storage_repo()
	result = await repo.download_file("string.pdf")
	print(result)
