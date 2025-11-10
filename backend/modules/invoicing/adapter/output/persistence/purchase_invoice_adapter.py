from dataclasses import dataclass
from typing import List, Sequence
from typing_extensions import override
from modules.invoicing.domain.entity import PurchaseInvoice
from modules.invoicing.domain.repository.purchase_invoice import (
	PurchaseInvoiceRepository,
)
from modules.invoicing.application.command import SearchPurchaseInvoiceCommand


@dataclass
class PurchaseInvoiceRepositoryAdapter(PurchaseInvoiceRepository):
	repository: PurchaseInvoiceRepository

	@override
	async def get_purchase_invoice_by_id(
		self, id_purchase_invoice: int
	) -> PurchaseInvoice | None:
		return await self.repository.get_purchase_invoice_by_id(id_purchase_invoice)

	@override
	async def get_purchase_invoice_list(
		self, limit: int, page: int
	) -> list[PurchaseInvoice] | Sequence[PurchaseInvoice]:
		return await self.repository.get_purchase_invoice_list(limit, page)

	@override
	async def get_purchase_invoice_list_by_provider(
		self, id_provider: int, limit: int, page: int
	) -> list[PurchaseInvoice] | Sequence[PurchaseInvoice]:
		return await self.repository.get_purchase_invoice_list_by_provider(
			id_provider, limit, page
		)

	@override
	async def save_purchase_invoice(
		self, purchase_invoice: PurchaseInvoice
	) -> PurchaseInvoice:
		return await self.repository.save_purchase_invoice(purchase_invoice)

	@override
	async def search_purchase_invoices(
		self, command: SearchPurchaseInvoiceCommand
	) -> tuple[List[PurchaseInvoice] | Sequence[PurchaseInvoice], int]:
		return await self.repository.search_purchase_invoices(command)
