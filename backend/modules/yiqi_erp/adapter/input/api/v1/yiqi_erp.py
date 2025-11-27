from io import BytesIO
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from modules.yiqi_erp.adapter.input.api.v1.request import (
	YiqiCreateAirWaybillRequest,
	YiqiUploadFileRequest,
)
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


@yiqi_erp_router.get("/country_list")
@inject
async def get_country_list(
	id_schema: int = Depends(Provide[YiqiContainer.config.YIQI_SCHEMA]),
	service: YiqiService = Depends(Provide[YiqiContainer.service]),
):
	return await service.get_country_list(id_schema)


@yiqi_erp_router.get("/country_list/{country_name}")
@inject
async def get_country_by_name(
	country_name: str,
	id_schema: int = Depends(Provide[YiqiContainer.config.YIQI_SCHEMA]),
	service: YiqiService = Depends(Provide[YiqiContainer.service]),
):
	return await service.get_country_by_name(country_name, id_schema)


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
	return await service.get_providers_list(id_schema)


@yiqi_erp_router.get("/provider/{id_provider}")
@inject
async def get_provider_by_id(
	id_provider: int,
	id_schema: int = Depends(Provide[YiqiContainer.config.YIQI_SCHEMA]),
	service: YiqiService = Depends(Provide[YiqiContainer.service]),
):
	return await service.get_provider_by_id(int(id_provider), id_schema)


@yiqi_erp_router.get("/air_waybills_template_file")
@inject
async def get_air_waybills_template_file(
	id_schema: int = Depends(Provide[YiqiContainer.config.YIQI_SCHEMA]),
	service: YiqiService = Depends(Provide[YiqiContainer.service]),
):
	file = await service.get_air_waybills_template_file(id_schema)
	headers = {"Content-Disposition": f'attachment; filename="{file.filename}"'}
	return StreamingResponse(
		content=BytesIO(file.file),
		headers=headers,
		media_type="application/octet-stream",
	)


@yiqi_erp_router.get("/air_waybills/{id_invoice}")
@inject
async def get_air_waybills_by_invoice_id(
	id_invoice: int,
	id_schema: int = Depends(Provide[YiqiContainer.config.YIQI_SCHEMA]),
	service: YiqiService = Depends(Provide[YiqiContainer.service]),
):
	return await service.get_air_waybills_by_invoice_id(int(id_invoice), id_schema)


@yiqi_erp_router.post("/create_air_waybill")
@inject
async def create_air_waybill(
	command: YiqiCreateAirWaybillRequest,
	id_schema: int = Depends(Provide[YiqiContainer.config.YIQI_SCHEMA]),
	service: YiqiService = Depends(Provide[YiqiContainer.service]),
):
	return await service.create_air_waybill(command, id_schema)


@yiqi_erp_router.post("/create_multiple_air_waybills")
@inject
async def create_multiple_air_waybills(
	upload_file: YiqiUploadFileRequest,
	id_schema: int = Depends(Provide[YiqiContainer.config.YIQI_SCHEMA]),
	service: YiqiService = Depends(Provide[YiqiContainer.service]),
):
	return await service.create_multiple_air_waybills(upload_file, id_schema)


@yiqi_erp_router.post("/upload_file")
@inject
async def upload_file(
	upload_file: YiqiUploadFileRequest,
	id_schema: int = Depends(Provide[YiqiContainer.config.YIQI_SCHEMA]),
	service: YiqiService = Depends(Provide[YiqiContainer.service]),
):
	return await service.upload_file(upload_file, id_schema)
