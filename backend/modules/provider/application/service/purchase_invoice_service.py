from dataclasses import dataclass
from typing import List, Sequence
from core.db import Transactional
from modules.provider.domain.command import (
	CreatePurchaseInvoiceServiceCommand,
	UpdatePurchaseInvoiceServiceCommand,
)
from modules.provider.domain.entity.purchase_invoice_service import (
	PurchaseInvoiceService,
)
from modules.provider.domain.exception import (
	DraftPurchaseInvoiceServiceNotFoundException,
)
from modules.provider.domain.repository.purchase_invoice_service import (
	PurchaseInvoiceServiceRepository,
)
from modules.provider.application.usecase.purchase_invoice_service import (
	PurchaseInvoiceServiceUseCaseFactory,
)


@dataclass
class PurchaseInvoiceServiceTypeService:
	purchase_invoice_service_repository: PurchaseInvoiceServiceRepository

	def __post_init__(self):
		self.purchase_invoice_service_usecase = PurchaseInvoiceServiceUseCaseFactory(
			self.purchase_invoice_service_repository
		)

	async def get_all_services(
		self, limit: int = 20, page: int = 0
	) -> list[PurchaseInvoiceService] | Sequence[PurchaseInvoiceService]:
		return await self.purchase_invoice_service_usecase.get_services_list(
			limit, page
		)

	async def get_services_by_id(
		self, id_purchase_invoice_service: int
	) -> PurchaseInvoiceService:
		purchase_invoice_service = (
			await self.purchase_invoice_service_usecase.get_service_by_id(
				id_purchase_invoice_service
			)
		)
		if not purchase_invoice_service:
			raise DraftPurchaseInvoiceServiceNotFoundException
		return purchase_invoice_service

	async def create_purchase_invoice_service(
		self, command: CreatePurchaseInvoiceServiceCommand
	) -> PurchaseInvoiceService:
		return self.purchase_invoice_service_usecase.create_invoice_service(command)

	@Transactional()
	async def save_purchase_invoice_service(
		self, purchase_invoice_service: PurchaseInvoiceService
	):
		return await self.purchase_invoice_service_usecase.save_purchase_invoice(
			purchase_invoice_service
		)

	@Transactional()
	async def delete_purchase_invoice_service(self, id_purchase_invoice_service: int):
		purchase_invoice_service = (
			await self.purchase_invoice_service_usecase.get_service_by_id(
				id_purchase_invoice_service
			)
		)
		if not purchase_invoice_service:
			raise DraftPurchaseInvoiceServiceNotFoundException
		return await self.purchase_invoice_service_usecase.delete_invoice_service(
			purchase_invoice_service
		)

	@Transactional()
	async def update_purchase_invoice_service(
		self, command: UpdatePurchaseInvoiceServiceCommand
	):
		return await self.purchase_invoice_service_usecase.update_invoice_service(
			command
		)

	async def get_services_of_provider(self, id_provider: int):
		return await self.purchase_invoice_service_usecase.get_services_of_provider(
			id_provider
		)

	async def add_services_to_provider(
		self, id_provider: int, id_services_list: List[int]
	):
		return await self.purchase_invoice_service_usecase.add_services_to_provider(
			id_provider, id_services_list
		)

	async def remove_services_from_provider(
		self, id_provider: int, id_services_list: List[int]
	):
		return (
			await self.purchase_invoice_service_usecase.remove_services_from_provider(
				id_provider, id_services_list
			)
		)
