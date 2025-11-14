from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends


from modules.yiqi_erp.adapter.input.api.v1.request import YiqiUploadFileRequest
from modules.yiqi_erp.application.service.yiqi import YiqiService
from modules.yiqi_erp.container import YiqiContainer


yiqi_erp_router = APIRouter()


@yiqi_erp_router.get("/currency_list")
@inject
async def get_currency_list(
	id_schema: int = Depends(Provide[YiqiContainer.config.YIQI_SCHEMA]),
	service: YiqiService = Depends(Provide[YiqiContainer.service]),
):
	return await service.get_currency_list(id_schema)


@yiqi_erp_router.get("/currency_list/{currency_code}")
@inject
async def get_currency_by_code(
	currency_code: str,
	id_schema: int = Depends(Provide[YiqiContainer.config.YIQI_SCHEMA]),
	service: YiqiService = Depends(Provide[YiqiContainer.service]),
):
	return await service.get_currency_by_code(currency_code, id_schema)


@yiqi_erp_router.get("/services_list")
@inject
async def get_services_list(
	id_schema: int = Depends(Provide[YiqiContainer.config.YIQI_SCHEMA]),
	service: YiqiService = Depends(Provide[YiqiContainer.service]),
):
	return await service.get_services_list(id_schema)


@yiqi_erp_router.get("/provider")
@inject
async def get_providers_list(
	id_schema: int = Depends(Provide[YiqiContainer.config.YIQI_SCHEMA]),
	service: YiqiService = Depends(Provide[YiqiContainer.service]),
):
	return await service.get_provider_by_id(int(id_provider), id_schema)


@yiqi_erp_router.get("/provider/{id_provider}")
@inject
async def get_provider_by_id(
	id_provider: int,
	id_schema: int = Depends(Provide[YiqiContainer.config.YIQI_SCHEMA]),
	service: YiqiService = Depends(Provide[YiqiContainer.service]),
):
	return await service.get_provider_by_id(int(id_provider), id_schema)


@yiqi_erp_router.post("/upload_file")
@inject
async def upload_file(
	upload_file: YiqiUploadFileRequest,
	id_schema: int = Depends(Provide[YiqiContainer.config.YIQI_SCHEMA]),
	service: YiqiService = Depends(Provide[YiqiContainer.service]),
):
	return await service.upload_file(upload_file, id_schema)
