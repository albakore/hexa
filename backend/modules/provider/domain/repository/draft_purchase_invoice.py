from abc import ABC, abstractmethod
from typing import Sequence

from modules.provider.domain.entity.draft_purchase_invoice import DraftPurchaseInvoice


class DraftPurchaseInvoiceRepository(ABC):
	@abstractmethod
	async def get_provider_draft_invoices_list(
		self, id_provider: int, limit: int = 12, page: int = 0
	) -> list[DraftPurchaseInvoice] | Sequence[DraftPurchaseInvoice]: ...

	@abstractmethod
	async def get_provider_draft_invoices_by_id(
		self, id_draft_purchase_invoice: int
	) -> DraftPurchaseInvoice | None: ...

	@abstractmethod
	async def save_draft_invoice(
		self, draft_purchase_invoice: DraftPurchaseInvoice
	) -> DraftPurchaseInvoice: ...

	@abstractmethod
	async def delete_draft_invoice(
		self, draft_purchase_invoice: DraftPurchaseInvoice
	): ...
