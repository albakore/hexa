from dataclasses import dataclass
from typing import Sequence
import uuid

from shared.interfaces.service_protocols import (
	CurrencyServiceProtocol,
	FileStorageServiceProtocol,
)
from modules.provider.application.dto import DraftPurchaseInvoiceDTO
from modules.provider.application.exception import (
	DraftPurchaseInvoiceCurrencyNotFoundException,
	DraftPurchaseInvoiceNotFoundException,
)
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
	file_storage_service: FileStorageServiceProtocol
	currency_service: CurrencyServiceProtocol | None

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

	async def get_draft_purchase_invoice_with_filemetadata(
		self, draft_purchase_invoice: DraftPurchaseInvoice
	) -> DraftPurchaseInvoiceDTO:
		archivo_comprobante = await self._get_metadata_or_none(
			draft_purchase_invoice.id_receipt_file
		)
		archivo_detalle = await self._get_metadata_or_none(
			draft_purchase_invoice.id_details_file
		)

		draft_invoice_dto = DraftPurchaseInvoiceDTO(
			**draft_purchase_invoice.model_dump(),
			receipt_file=archivo_comprobante,
			details_file=archivo_detalle,
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

	async def finalize_draft(self, id_draft_purchase_invoice: int):
		"""
		Finaliza un draft marcándolo como listo para ser procesado.
		Solo valida y cambia el estado, NO crea facturas.
		"""
		draft_invoice = await self.get_draft_purchase_invoice_by_id(
			id_draft_purchase_invoice
		)

		if not draft_invoice.currency:
			raise DraftPurchaseInvoiceCurrencyNotFoundException

		if not draft_invoice.id_receipt_file:
			raise ValueError("El archivo de comprobante es requerido")

		draft_invoice.state = "Finalized"
		await self.save_draft_purchase_invoice(draft_invoice)
		return draft_invoice

	async def _get_metadata_or_none(self, file_id: uuid.UUID | None):
		if not file_id:
			return None
		try:
			metadata = await self.file_storage_service().get_metadata(file_id)
			return metadata
		except Exception as e:
			print("Hubo un error al obtener la metadata:", e)
			return None
