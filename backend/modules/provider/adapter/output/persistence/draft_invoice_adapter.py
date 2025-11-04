from dataclasses import dataclass
from typing import List, Sequence
from modules.provider.domain.entity.draft_purchase_invoice import DraftPurchaseInvoice
from modules.provider.domain.repository.draft_purchase_invoice import (
	DraftPurchaseInvoiceRepository,
)
from modules.provider.domain.command import SearchDraftPurchaseInvoiceCommand


class DraftPurchaseInvoiceAdapter(DraftPurchaseInvoiceRepository):
	def __init__(
		self, draft_purchase_invoice_repository: DraftPurchaseInvoiceRepository
	):
		self.draft_purchase_invoice_repository = draft_purchase_invoice_repository

	async def get_provider_draft_invoices_list(
		self, id_provider: int, limit: int = 12, page: int = 0
	) -> list[DraftPurchaseInvoice] | Sequence[DraftPurchaseInvoice]:
		return await self.draft_purchase_invoice_repository.get_provider_draft_invoices_list(
			id_provider, limit, page
		)

	async def get_provider_draft_invoices_by_id(
		self, id_draft_purchase_invoice: int
	) -> DraftPurchaseInvoice | None:
		return await self.draft_purchase_invoice_repository.get_provider_draft_invoices_by_id(
			id_draft_purchase_invoice
		)

	async def save_draft_invoice(
		self, draft_purchase_invoice: DraftPurchaseInvoice
	) -> DraftPurchaseInvoice:
		return await self.draft_purchase_invoice_repository.save_draft_invoice(
			draft_purchase_invoice
		)

	async def delete_draft_invoice(self, draft_purchase_invoice: DraftPurchaseInvoice):
		return await self.draft_purchase_invoice_repository.delete_draft_invoice(
			draft_purchase_invoice
		)

	async def search_draft_invoices(
		self, command: SearchDraftPurchaseInvoiceCommand
	) -> tuple[List[DraftPurchaseInvoice] | Sequence[DraftPurchaseInvoice], int]:
		return await self.draft_purchase_invoice_repository.search_draft_invoices(command)
