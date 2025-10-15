from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Sequence, TypedDict

from modules.invoicing.domain.entity import PurchaseInvoice


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
