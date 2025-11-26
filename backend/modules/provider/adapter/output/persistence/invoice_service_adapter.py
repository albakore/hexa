from typing import List, Sequence

from modules.provider.application.dto import ProviderServiceWithRequirementsDTO
from modules.provider.domain.command import SearchPurchaseInvoiceServiceCommand
from modules.provider.domain.entity import PurchaseInvoiceService
from modules.provider.domain.entity.purchase_invoice_service import (
	ProviderInvoiceServiceLink,
)
from modules.provider.domain.repository.purchase_invoice_service import (
	PurchaseInvoiceServiceRepository,
)


class PurchaseInvoiceServiceRepositoryAdapter(PurchaseInvoiceServiceRepository):
	def __init__(
		self, purchase_invoice_service_repository: PurchaseInvoiceServiceRepository
	):
		self.purchase_invoice_service_repository = purchase_invoice_service_repository

	async def get_services_list(
		self, limit: int = 1000, page: int = 0
	) -> list[PurchaseInvoiceService] | Sequence[PurchaseInvoiceService]:
		return await self.purchase_invoice_service_repository.get_services_list(
			limit, page
		)

	async def get_services_by_id(
		self, id_provider: int
	) -> PurchaseInvoiceService | None:
		return await self.purchase_invoice_service_repository.get_services_by_id(
			id_provider
		)

	async def save_service(
		self, invoice_service: PurchaseInvoiceService
	) -> PurchaseInvoiceService | None:
		return await self.purchase_invoice_service_repository.save_service(
			invoice_service
		)

	async def delete_service(self, invoice_service: PurchaseInvoiceService):
		return await self.purchase_invoice_service_repository.delete_service(
			invoice_service
		)

	async def get_services_of_provider(
		self, id_provider: int
	) -> List[ProviderServiceWithRequirementsDTO]:
		return await self.purchase_invoice_service_repository.get_services_of_provider(
			id_provider
		)

	async def add_services_to_provider(
		self, id_provider: int, id_services_list: List[int]
	) -> None:
		return await self.purchase_invoice_service_repository.add_services_to_provider(
			id_provider, id_services_list
		)

	async def remove_services_from_provider(
		self, id_provider: int, id_services_list: List[int]
	) -> None:
		return await self.purchase_invoice_service_repository.remove_services_from_provider(
			id_provider, id_services_list
		)

	async def get_provider_service_link(
		self, id_provider: int, id_service: int
	) -> ProviderInvoiceServiceLink | None:
		return await self.purchase_invoice_service_repository.get_provider_service_link(
			id_provider, id_service
		)

	async def search_services(
		self, command: SearchPurchaseInvoiceServiceCommand
	) -> tuple[List[PurchaseInvoiceService] | Sequence[PurchaseInvoiceService], int]:
		return await self.purchase_invoice_service_repository.search_services(command)
