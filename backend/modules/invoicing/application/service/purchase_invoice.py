from dataclasses import dataclass
from typing import Callable

from celery import Celery

from modules.invoicing.application.command import CreatePurchaseInvoiceCommand
from modules.invoicing.application.dto import PurchaseInvoiceDTO
from modules.invoicing.domain.entity.purchase_invoice import PurchaseInvoice
from modules.invoicing.domain.repository.purchase_invoice import (
	PurchaseInvoiceRepository,
)
from modules.invoicing.domain.usecase.purchase_invoice import InvoiceUseCaseFactory
from core.db.transactional import Transactional
from shared.interfaces.service_protocols import YiqiERPTasksProtocol


@dataclass
class PurchaseInvoiceService:
	purchase_invoice_repository: PurchaseInvoiceRepository
	tasks_service: Celery

	def __post_init__(self):
		self.usecase = InvoiceUseCaseFactory(self.purchase_invoice_repository)

	async def get_list(self, limit: int, page: int):
		return await self.usecase.get_purchase_invoice_list(limit, page)

	async def get_list_of_provider(self, id_provider: int, limit: int, page: int):
		return await self.usecase.get_purchase_invoice_list_by_provider(
			id_provider, limit, page
		)

	async def get_one_by_id(self, id_purchase_invoice: int):
		return await self.usecase.get_purchase_invoice_by_id(id_purchase_invoice)

	async def create(self, command: CreatePurchaseInvoiceCommand | dict):
		purchase_invoice = PurchaseInvoice.model_validate(command)
		return purchase_invoice

	@Transactional()
	async def save(self, purchase_invoice_dto: PurchaseInvoice):
		return await self.usecase.save_purchase_invoice(purchase_invoice_dto)

	@Transactional()
	async def save_and_emit(
		self, purchase_invoice_dto: PurchaseInvoice
	) -> PurchaseInvoice:
		purchase_invoice = await self.usecase.save_purchase_invoice(
			purchase_invoice_dto
		)
		self.tasks_service.send_task(
			"yiqi_erp.create_invoice_from_purchase_invoice_tasks",
			args=[purchase_invoice.id],
			countdown=30,
		)
		return purchase_invoice

	async def reemit(self, id_purchase_invoice: int):
		purchase_invoice = await self.usecase.get_purchase_invoice_by_id(
			id_purchase_invoice
		)

		self.tasks_service.send_task(
			"yiqi_erp.create_invoice_from_purchase_invoice_tasks",
			args=[purchase_invoice.id],
			countdown=30,
		)
		return purchase_invoice
