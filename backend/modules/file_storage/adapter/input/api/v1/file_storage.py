from io import BytesIO
from re import A
from typing import Annotated
import uuid
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Form, Query, Response, UploadFile
from fastapi.params import File
from fastapi.responses import FileResponse, StreamingResponse

from modules.file_storage.application.dto import FileStorageDTO
from modules.file_storage.container import FileStorageContainer

# from modules.file_storage.adapter.input.api.v1.request import ProviderCreateRequest, ProviderUpdateRequest
from modules.file_storage.application.service.file_storage import FileStorageService
from modules.file_storage.domain.command import SaveFileCommand

DepsFileStorageService = Annotated[
	FileStorageService, Depends(Provide[FileStorageContainer.service])
]

file_storage_router = APIRouter()


@file_storage_router.post("/upload")
@inject
async def upload_file(
	file: UploadFile,
	service: DepsFileStorageService,
):
	print(file.filename)
	command = SaveFileCommand(
		file=file.file, filename=file.filename or "undefined_file", size=file.size
	)
	return await service.save_file(command)


@file_storage_router.post("/{uuid_file}/download")
@inject
async def download_file(
	uuid_file: uuid.UUID,
	service: DepsFileStorageService,
):
	file_dto = await service.download_file(uuid_file)
	headers = {
		"Content-Disposition": f'attachment; filename="{file_dto.metadata.download_filename}"'
	}
	return StreamingResponse(
		content=BytesIO(file_dto.file),
		headers=headers,
		media_type="application/octet-stream",
	)


@file_storage_router.get("/{uuid_file}")
@inject
async def get_file_metadata(
	uuid_file: uuid.UUID,
	service: DepsFileStorageService,
):
	return await service.get_metadata(uuid_file)
