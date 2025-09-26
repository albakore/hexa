from typing import BinaryIO
import uuid
import pytest
from shared.file_storage.container import FileStorageContainer
from faker import Faker

from shared.file_storage.domain.command import SaveFileCommand
from core.db.session import set_session_context, reset_session_context

faker = Faker()


@pytest.mark.asyncio
async def test_upload_file():
	session_uuid = uuid.uuid4()
	context = set_session_context(str(session_uuid))
	service = FileStorageContainer().service()
	with open("shared/file_storage/test/string.pdf", "rb") as f:
		command = SaveFileCommand(file=f, filename=f.name)
		result = await service.save_file(command)
		print(result)
	reset_session_context(context)
