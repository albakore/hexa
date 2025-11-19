from abc import ABC, abstractmethod
from typing import List, Sequence

from modules.provider.application.dto import ProviderServiceWithRequirementsDTO
from modules.provider.domain.entity.purchase_invoice_service import (
	PurchaseInvoiceService,
	ProviderInvoiceServiceLink,
)


class PurchaseInvoiceServiceRepository(ABC):
	@abstractmethod
	async def get_services_list(
		self, limit: int = 12, page: int = 0
	) -> list[PurchaseInvoiceService] | Sequence[PurchaseInvoiceService]: ...

	@abstractmethod
	async def get_services_by_id(
		self, id_service: int
	) -> PurchaseInvoiceService | None: ...

	@abstractmethod
	async def save_service(
		self, invoice_service: PurchaseInvoiceService
	) -> PurchaseInvoiceService | None: ...

	@abstractmethod
	async def delete_service(self, invoice_service: PurchaseInvoiceService): ...

	@abstractmethod
	async def get_services_of_provider(
		self, id_provider: int
	) -> List[ProviderServiceWithRequirementsDTO]: ...

	@abstractmethod
	async def add_services_to_provider(
		self, id_provider: int, services: List
	) -> None: ...

	@abstractmethod
	async def remove_services_from_provider(
		self, id_provider: int, id_services_list: List[int]
	) -> None: ...

	@abstractmethod
	async def get_provider_service_link(
		self, id_provider: int, id_service: int
	) -> ProviderInvoiceServiceLink | None: ...
