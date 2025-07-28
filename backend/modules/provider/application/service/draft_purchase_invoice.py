from dataclasses import dataclass
from typing import Sequence
from modules.provider.application.exception import DraftPurchaseInvoiceNotFoundException
from modules.provider.domain.command import CreateDraftPurchaseInvoiceCommand
from modules.provider.domain.entity.draft_purchase_invoice import DraftPurchaseInvoice
from modules.provider.domain.repository.draft_purchase_invoice import (
	DraftPurchaseInvoiceRepository,
)
from modules.provider.domain.usecase.draft_purchase_invoice import (
	DraftPurchaseInvoiceUseCaseFactory,
)


@dataclass
class DraftPurchaseInvoiceService:
	draft_purchase_invoice_repository: DraftPurchaseInvoiceRepository

	def __post_init__(self):
		self.draft_purchase_invoice_usecase = DraftPurchaseInvoiceUseCaseFactory(
			self.draft_purchase_invoice_repository
		)

	async def get_all_draft_purchase_invoices(
		self, id_provider: int, limit: int = 20, page: int = 0
	) -> list[DraftPurchaseInvoice] | Sequence[DraftPurchaseInvoice]:
		return (
			await self.draft_purchase_invoice_usecase.get_provider_draft_invoices_list(
				id_provider, limit, page
			)
		)

	async def get_draft_purchase_invoice_by_id(
		self, id_draft_purchase_invoice: int
	) -> DraftPurchaseInvoice:
		draft_purchase_invoice = (
			await self.draft_purchase_invoice_usecase.get_draft_purchase_invoice_by_id(
				id_draft_purchase_invoice
			)
		)
		if not draft_purchase_invoice:
			raise DraftPurchaseInvoiceNotFoundException
		return draft_purchase_invoice

	async def create_draft_purchase_invoice(
		self, command: CreateDraftPurchaseInvoiceCommand
	) -> DraftPurchaseInvoice:
		return self.draft_purchase_invoice_usecase.create_draft_purchase_invoice(
			command
		)

	async def save_draft_purchase_invoice(
		self, draft_purchase_invoice: DraftPurchaseInvoice
	):
		return await self.draft_purchase_invoice_usecase.save_draft_purchase_invoice(
			draft_purchase_invoice
		)

	async def delete_draft_purchase_invoice(self, id_draft_purchase_invoice: int):
		draft_purchase_invoice = (
			await self.draft_purchase_invoice_usecase.get_draft_purchase_invoice_by_id(
				id_draft_purchase_invoice
			)
		)
		if not draft_purchase_invoice:
			raise DraftPurchaseInvoiceNotFoundException
		return await self.draft_purchase_invoice_usecase.delete_draft_purchase_invoice(
			draft_purchase_invoice
		)
