from dataclasses import dataclass

import httpx

from modules.yiqi_erp.application.exception import (
	YiqiEntityNotFoundException,
	YiqiServiceException,
)
from modules.yiqi_erp.domain.command import CreateYiqiInvoiceCommand, UploadFileCommand
from modules.yiqi_erp.domain.repository.yiqi import YiqiRepository


@dataclass
class CreateInvoiceUseCase:
	yiqi_repository: YiqiRepository

	async def __call__(self, command: CreateYiqiInvoiceCommand, id_schema: int) -> dict:
		invoice = await self.yiqi_repository.create_invoice(command, id_schema)
		return invoice


@dataclass
class GetProviderByIdUseCase:
	yiqi_repository: YiqiRepository

	async def __call__(self, id_provider: int, id_schema: int):
		provider = await self.yiqi_repository.get_provider_by_id(id_provider, id_schema)
		if provider.is_success:
			return provider.json()
		if provider.is_client_error:
			raise YiqiEntityNotFoundException

		raise YiqiServiceException


@dataclass
class GetServicesListUseCase:
	yiqi_repository: YiqiRepository

	async def __call__(self, id_schema: int):
		response = await self.yiqi_repository.get_services_list(id_schema)
		if response.is_success:
			return response.json()
		raise YiqiServiceException


@dataclass
class GetCurrencyListUseCase:
	yiqi_repository: YiqiRepository

	async def __call__(self, id_schema: int):
		response: httpx.Response = await self.yiqi_repository.get_currency_list(
			id_schema
		)
		if response.is_success:
			return response.json()
		raise YiqiServiceException


@dataclass
class GetCurrencyByCodeUseCase:
	yiqi_repository: YiqiRepository

	async def __call__(self, code: str, id_schema: int) -> dict | None:
		response: httpx.Response = await self.yiqi_repository.get_currency_by_code(
			code, id_schema
		)
		if response.is_success:
			try:
				return response.json()[0]
			except (Exception, IndexError, KeyError):
				return None
		raise YiqiServiceException


@dataclass
class UploadFileUseCase:
	yiqi_repository: YiqiRepository

	async def __call__(self, command: UploadFileCommand, id_schema: int):
		response: httpx.Response = await self.yiqi_repository.upload_file(
			command, id_schema
		)
		if response.is_success:
			return True
		raise YiqiServiceException


@dataclass
class YiqiUseCaseFactory:
	yiqi_repository: YiqiRepository

	def __post_init__(self):
		self.create_invoice = CreateInvoiceUseCase(self.yiqi_repository)
		self.get_provider_by_id = GetProviderByIdUseCase(self.yiqi_repository)
		self.get_services_list = GetServicesListUseCase(self.yiqi_repository)
		self.get_currency_list = GetCurrencyListUseCase(self.yiqi_repository)
		self.get_currency_by_code = GetCurrencyByCodeUseCase(self.yiqi_repository)
		self.upload_file = UploadFileUseCase(self.yiqi_repository)
