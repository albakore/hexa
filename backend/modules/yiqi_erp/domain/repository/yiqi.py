from abc import ABC, abstractmethod

from fastapi import UploadFile

from modules.yiqi_erp.domain.command import CreateYiqiInvoiceCommand


class YiqiRepository(ABC):
	@abstractmethod
	async def get_provider_by_id(self, id_provider: int, id_schema: int): ...

	@abstractmethod
	async def get_contact_by_id(self, id_contact: int, id_schema: int): ...

	@abstractmethod
	async def get_services_list(self, id_schema: int): ...

	@abstractmethod
	async def get_services_list_by_provider_id(
		self, id_provider: int, id_schema: int
	): ...

	@abstractmethod
	async def get_currency_list(self, id_schema: int): ...

	@abstractmethod
	async def get_currency_by_code(self, code: str, id_schema: int) -> list[dict]: ...

	@abstractmethod
	async def get_country_list(self, id_schema: int): ...

	@abstractmethod
	async def get_country_by_name(
		self, country_name: str, id_schema: int
	) -> dict | None: ...

	@abstractmethod
	async def get_invoices_list_of_provider(self, id_provider: int, id_schema: int): ...

	@abstractmethod
	async def create_invoice(
		self,
		command: CreateYiqiInvoiceCommand,
		id_schema: int,
		id_parent: bool | None = None,
		id_child: bool | None = None,
		id_entity: int = 660,
	) -> dict: ...

	@abstractmethod
	async def upload_file(self, file: UploadFile, id_schema: int): ...
