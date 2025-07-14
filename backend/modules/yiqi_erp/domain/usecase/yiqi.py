
from dataclasses import dataclass

from fastapi import UploadFile

from modules.yiqi_erp.domain.command import CreateYiqiInvoiceCommand, UploadFileCommand
from modules.yiqi_erp.domain.repository.yiqi import YiqiRepository

@dataclass
class CreateInvoiceUseCase:
	yiqi_repository : YiqiRepository

	async def __call__(self, command : CreateYiqiInvoiceCommand, id_schema: int):
		invoice = await self.yiqi_repository.create_invoice(command, id_schema)
		return invoice

@dataclass
class GetProviderByIdUseCase:
	yiqi_repository : YiqiRepository

	async def __call__(self, id_provider : int, id_schema : int):
		provider = await self.yiqi_repository.get_provider_by_id(id_provider, id_schema)
		return provider

@dataclass
class GetServicesListUseCase:
	yiqi_repository : YiqiRepository

	async def __call__(self, id_schema : int):
		response = await self.yiqi_repository.get_services_list(id_schema)
		return response

@dataclass
class GetCurrencyListUseCase:
	yiqi_repository : YiqiRepository

	async def __call__(self, id_schema : int):
		response = await self.yiqi_repository.get_currency_list(id_schema)
		return response

@dataclass
class UploadFileUseCase:
	yiqi_repository : YiqiRepository

	async def __call__(self, command : UploadFileCommand, id_schema : int):
		response = await self.yiqi_repository.upload_file(command,id_schema)
		return response


@dataclass
class YiqiUseCaseFactory:
	yiqi_repository : YiqiRepository

	def __post_init__(self):
		self.create_invoice = CreateInvoiceUseCase(self.yiqi_repository)
		self.get_provider_by_id = GetProviderByIdUseCase(self.yiqi_repository)
		self.get_services_list = GetServicesListUseCase(self.yiqi_repository)
		self.get_currency_list = GetCurrencyListUseCase(self.yiqi_repository)
		self.upload_file = UploadFileUseCase(self.yiqi_repository)