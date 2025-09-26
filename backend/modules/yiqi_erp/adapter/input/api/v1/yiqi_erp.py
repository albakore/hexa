from fastapi import APIRouter, Depends
from shared.dependencies import get_yiqi_service

from modules.yiqi_erp.adapter.input.api.v1.request import YiqiUploadFileRequest

yiqi_erp_router = APIRouter()


@yiqi_erp_router.get("/currency_list")
async def get_currency_list(
	id_schema: int = 1,
	service = Depends(get_yiqi_service),
):
	return await service.get_currency_list(id_schema)


@yiqi_erp_router.get("/currency_list/{currency_code}")
async def get_currency_by_code(
	currency_code: str,
	id_schema: int = 1,
	service = Depends(get_yiqi_service),
):
	return await service.get_currency_by_code(currency_code, id_schema)


@yiqi_erp_router.get("/services_list")
async def get_services_list(
	id_schema: int = 1,
	service = Depends(get_yiqi_service),
):
	return await service.get_services_list(id_schema)


@yiqi_erp_router.get("/provider/{id_provider}")
async def get_provider_by_id(
	id_provider: int,
	id_schema: int = 1,
	service = Depends(get_yiqi_service),
):
	return await service.get_provider_by_id(int(id_provider), id_schema)


@yiqi_erp_router.post("/upload_file")
async def upload_file(
	upload_file: YiqiUploadFileRequest,
	id_schema: int = 1,
	service = Depends(get_yiqi_service),
):
	return await service.upload_file(upload_file, id_schema)
