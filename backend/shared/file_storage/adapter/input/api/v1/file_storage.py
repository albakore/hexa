from io import BytesIO
import uuid
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Form, Query, Response, UploadFile
from fastapi.params import File
from fastapi.responses import FileResponse, StreamingResponse

from shared.container import SharedContainer
from shared.file_storage.application.dto import FileStorageDTO
from shared.file_storage.container import FileStorageContainer
# from shared.file_storage.adapter.input.api.v1.request import ProviderCreateRequest, ProviderUpdateRequest
from shared.file_storage.application.service.file_storage import FileStorageService
from shared.file_storage.domain.command import SaveFileCommand




file_storage_router = APIRouter()

@file_storage_router.post("/upload")
@inject
async def upload_file(
	file : UploadFile,
	service : FileStorageService = Depends(Provide[SharedContainer.file_storage.service])
):
	print(file.filename)
	command = SaveFileCommand(
		file=file.file,
		filename=file.filename or "undefined_file",
		size=file.size
	)
	return await service.save_file(command)

@file_storage_router.post("/{uuid_file}/download")
@inject
async def download_file(
	uuid_file : uuid.UUID,
	service : FileStorageService = Depends(Provide[SharedContainer.file_storage.service])
):
	
	file_dto = await service.download_file(uuid_file)	
	headers = {
		"Content-Disposition": f'attachment; filename="{file_dto.metadata.download_filename}"'
	}
	return StreamingResponse(
		content=BytesIO(file_dto.file),
		headers=headers,
		media_type="application/octet-stream"
	)

@file_storage_router.get("/{uuid_file}")
@inject
async def get_file_metadata(
	uuid_file : uuid.UUID,
	service : FileStorageService = Depends(Provide[SharedContainer.file_storage.service])
):
	
	return await service.get_metadata(uuid_file)	
