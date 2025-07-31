from dataclasses import dataclass
from typing import Sequence

from core.db import Transactional
from modules.provider.domain.command import CreateDraftPurchaseInvoiceCommand
from modules.provider.domain.entity.draft_purchase_invoice import DraftPurchaseInvoice
from modules.provider.domain.repository.draft_purchase_invoice import (
	DraftPurchaseInvoiceRepository,
)


@dataclass
class GetProviderDraftInvoicesListUseCase:
	draft_purchase_invoice_repository: DraftPurchaseInvoiceRepository

	async def __call__(
		self, id_provider: int, limit: int = 50, page: int = 0
	) -> list[DraftPurchaseInvoice] | Sequence[DraftPurchaseInvoice]:
		return await self.draft_purchase_invoice_repository.get_provider_draft_invoices_list(
			id_provider, limit, page
		)


@dataclass
class GetDraftPurchaseInvoicesByIdUseCase:
	draft_purchase_invoice_repository: DraftPurchaseInvoiceRepository

	async def __call__(
		self, id_draft_purchase_invoice: int
	) -> DraftPurchaseInvoice | None:
		return await self.draft_purchase_invoice_repository.get_provider_draft_invoices_by_id(
			id_draft_purchase_invoice
		)


@dataclass
class CreateDraftPurchaseInvoiceUseCase:
	def __call__(
		self, command: CreateDraftPurchaseInvoiceCommand
	) -> DraftPurchaseInvoice:
		return DraftPurchaseInvoice.model_validate(command)


@dataclass
class SaveDraftPurchaseInvoicesUseCase:
	draft_purchase_invoice_repository: DraftPurchaseInvoiceRepository

	@Transactional()
	async def __call__(
		self, draft_purchase_invoice: DraftPurchaseInvoice
	) -> DraftPurchaseInvoice | None:
		return await self.draft_purchase_invoice_repository.save_draft_invoice(
			draft_purchase_invoice
		)


@dataclass
class DeleteDraftPurchaseInvoicesUseCase:
	draft_purchase_invoice_repository: DraftPurchaseInvoiceRepository

	@Transactional()
	async def __call__(self, draft_purchase_invoice: DraftPurchaseInvoice) -> None:
		return await self.draft_purchase_invoice_repository.delete_draft_invoice(
			draft_purchase_invoice
		)


@dataclass
class DraftPurchaseInvoiceUseCaseFactory:
	draft_purchase_invoice_repository: DraftPurchaseInvoiceRepository

	def __post_init__(self):
		self.get_provider_draft_invoices_list = GetProviderDraftInvoicesListUseCase(
			self.draft_purchase_invoice_repository
		)
		self.get_draft_purchase_invoice_by_id = GetDraftPurchaseInvoicesByIdUseCase(
			self.draft_purchase_invoice_repository
		)
		self.create_draft_purchase_invoice = CreateDraftPurchaseInvoiceUseCase()
		self.save_draft_purchase_invoice = SaveDraftPurchaseInvoicesUseCase(
			self.draft_purchase_invoice_repository
		)
		self.delete_draft_purchase_invoice = DeleteDraftPurchaseInvoicesUseCase(
			self.draft_purchase_invoice_repository
		)
