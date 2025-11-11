from abc import ABC, abstractmethod
from typing import List, Sequence

from modules.invoicing.domain.entity import PurchaseInvoice
from modules.invoicing.application.command import SearchPurchaseInvoiceCommand


class PurchaseInvoiceRepository(ABC):
	@abstractmethod
	async def get_purchase_invoice_by_id(
		self, id_purchase_invoice: int
	) -> PurchaseInvoice | None: ...

	@abstractmethod
	async def get_purchase_invoice_list(
		self, limit: int, page: int
	) -> list[PurchaseInvoice] | Sequence[PurchaseInvoice]: ...

	@abstractmethod
	async def get_purchase_invoice_list_by_provider(
		self, id_provider: int, limit: int, page: int
	) -> list[PurchaseInvoice] | Sequence[PurchaseInvoice]: ...

	@abstractmethod
	async def save_purchase_invoice(
		self, purchase_invoice: PurchaseInvoice
	) -> PurchaseInvoice: ...

	@abstractmethod
	async def search_purchase_invoices(
		self, command: SearchPurchaseInvoiceCommand
	) -> tuple[List[PurchaseInvoice] | Sequence[PurchaseInvoice], int]: ...

	# Devuelve (lista_resultados, total_encontrado)
