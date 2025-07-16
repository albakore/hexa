from typing import BinaryIO
import pytest
from shared.file_storage.container import FileStorageContainer
from faker import Faker
faker = Faker()

@pytest.mark.asyncio
async def test_upload_file():
	repo = FileStorageContainer().s3_storage_repo()
	with open("/shared/file_storage/test/string.pdf","r") as f:
		result = repo.upload_file(f,faker.file_name())	
		print(result)