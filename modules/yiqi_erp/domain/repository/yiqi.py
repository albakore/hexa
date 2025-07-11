
from abc import ABC, abstractmethod

from modules.yiqi_erp.domain.command import CreateYiqiInvoiceCommand


class YiqiRepository(ABC):
	
	@abstractmethod
	async def get_provider_by_id(self, id_provider : int) : ...

	@abstractmethod
	async def get_contact_by_id(self, id_contact : int) : ...

	@abstractmethod
	async def get_services_list(self) : ...

	@abstractmethod
	async def get_services_list_by_provider_id(self, id_provider: int) : ...

	@abstractmethod
	async def get_currency_list(self) : ...

	@abstractmethod
	async def get_invoices_list_of_provider(self, id_provider: int) : ...

	@abstractmethod
	async def create_invoice(self, command: CreateYiqiInvoiceCommand) : ...