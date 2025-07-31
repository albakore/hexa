from dataclasses import dataclass
from typing import Sequence
import uuid
from modules.provider.application.dto import DraftPurchaseInvoiceDTO
from modules.provider.application.exception import DraftPurchaseInvoiceNotFoundException
from modules.provider.domain.command import CreateDraftPurchaseInvoiceCommand
from modules.provider.domain.entity.draft_purchase_invoice import DraftPurchaseInvoice
from modules.provider.domain.repository.draft_purchase_invoice import (
	DraftPurchaseInvoiceRepository,
)
from modules.provider.domain.usecase.draft_purchase_invoice import (
	DraftPurchaseInvoiceUseCaseFactory,
)
from shared import file_storage
from shared.file_storage.application.service.file_storage import FileStorageService


@dataclass
class DraftPurchaseInvoiceService:
	draft_purchase_invoice_repository: DraftPurchaseInvoiceRepository
	file_storage_service: FileStorageService

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
	) -> DraftPurchaseInvoiceDTO:
		draft_purchase_invoice = (
			await self.draft_purchase_invoice_usecase.get_draft_purchase_invoice_by_id(
				id_draft_purchase_invoice
			)
		)
		if not draft_purchase_invoice:
			raise DraftPurchaseInvoiceNotFoundException

		archivo_comprobante = await self._get_metadata_or_none(draft_purchase_invoice.id_archivo_comprobante)
		archivo_detalle = await self._get_metadata_or_none(draft_purchase_invoice.id_archivo_detalle)

		draft_invoice_dto = DraftPurchaseInvoiceDTO(
			**draft_purchase_invoice.model_dump(),
			archivo_comprobante=archivo_comprobante,
			archivo_detalle=archivo_detalle,
		)
		return draft_invoice_dto

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

	async def _get_metadata_or_none(self, file_id: uuid.UUID | None):
		if not file_id:
			return None
		try:
			return await self.file_storage_service.get_metadata(file_id)
		except Exception:
			return None