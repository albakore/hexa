from dataclasses import dataclass

from modules.yiqi_erp.domain.command import (
	CreateYiqiAirWaybillCommand,
	CreateYiqiInvoiceCommand,
	UploadFileCommand,
)
from modules.yiqi_erp.domain.repository.yiqi import YiqiRepository
from modules.yiqi_erp.application.usecase.yiqi import YiqiUseCaseFactory


@dataclass
class YiqiService:
	yiqi_repository: YiqiRepository

	def __post_init__(self):
		self.usecase = YiqiUseCaseFactory(self.yiqi_repository)

	async def create_invoice(
		self, command: CreateYiqiInvoiceCommand, id_schema: int
	) -> dict:
		return await self.usecase.create_invoice(command, id_schema)

	async def create_air_waybill(
		self, command: CreateYiqiAirWaybillCommand, id_schema: int
	) -> dict:
		return await self.usecase.create_air_waybill(command, id_schema)

	async def create_multiple_air_waybills(
		self, command: UploadFileCommand, id_schema: int
	):
		return await self.usecase.create_multiple_air_waybills(command, id_schema)

	async def get_air_waybills_template_file(self, id_schema: int):
		return await self.usecase.get_air_waybills_template_file(id_schema)

	async def get_air_waybills_by_invoice_id(self, id_invoice: int, id_schema: int):
		return await self.usecase.get_air_waybills_by_invoice_id(id_invoice, id_schema)

	async def get_provider_by_id(self, id_provider: int, id_schema: int):
		return await self.usecase.get_provider_by_id(id_provider, id_schema)

	async def get_providers_list(self, id_schema: int):
		return await self.usecase.get_providers_list(id_schema)

	async def get_services_list(self, id_schema: int):
		return await self.usecase.get_services_list(id_schema)

	async def get_currency_list(self, id_schema: int):
		return await self.usecase.get_currency_list(id_schema)

	async def get_currency_by_code(self, code: str, id_schema: int):
		return await self.usecase.get_currency_by_code(code, id_schema)

	async def get_country_list(self, id_schema: int):
		return await self.usecase.get_country_list(id_schema)

	async def get_country_by_name(self, country_name: str, id_schema: int):
		return await self.usecase.get_country_by_name(country_name, id_schema)

	async def upload_file(self, command: UploadFileCommand, id_schema: int):
		return await self.usecase.upload_file(command, id_schema)
