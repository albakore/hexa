from dataclasses import dataclass
from typing import List, Sequence
import uuid

from core.db.transactional import Transactional
from modules.provider.application.service.purchase_invoice_service import (
	PurchaseInvoiceServiceTypeService,
)
from shared.interfaces.service_protocols import (
	CurrencyServiceProtocol,
	FileStorageServiceProtocol,
	PurchaseInvoiceServiceProtocol,
)
from modules.provider.application.dto import DraftPurchaseInvoiceDTO
from modules.provider.application.exception import (
	DraftPurchaseInvoiceCurrencyNotFoundException,
	DraftPurchaseInvoiceDetailFileInvalidException,
	DraftPurchaseInvoiceNotFoundException,
	DraftPurchaseInvoiceReceiptFileInvalidException,
	DraftPurchaseInvoiceServiceNotFoundException,
)
from modules.provider.domain.command import (
	CreateDraftPurchaseInvoiceCommand,
	SearchDraftPurchaseInvoiceCommand,
)
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
	draft_purchase_invoice_servicetype_service: PurchaseInvoiceServiceTypeService
	purchase_invoice_service: PurchaseInvoiceServiceProtocol
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

	async def search_draft_purchase_invoices(
		self, command: SearchDraftPurchaseInvoiceCommand
	) -> tuple[List[DraftPurchaseInvoice] | Sequence[DraftPurchaseInvoice], int]:
		return await self.draft_purchase_invoice_usecase.search_draft_purchase_invoices(
			command
		)

	@Transactional()
	async def finalize_draft(self, id_draft_purchase_invoice: int):
		"""
		Valida, finaliza el draft y crea la factura asociada.

		Flujo:
		1. Valida archivos en storage (capa aplicación)
		2. Valida campos obligatorios (capa dominio)
		3. Marca como "Finalized"
		4. Crea PurchaseInvoice asociada
		5. Vincula factura con draft

		Returns:
			PurchaseInvoice creada
		"""
		# Obtener draft
		draft_invoice = await self.get_draft_purchase_invoice_by_id(
			id_draft_purchase_invoice
		)

		# Si ya tiene factura asociada, retornar la factura existente
		if draft_invoice.fk_invoice:
			return await self.purchase_invoice_service().get_one_by_id(
				draft_invoice.fk_invoice
			)

		# Obtener configuración del servicio
		if not draft_invoice.fk_invoice_service:
			raise DraftPurchaseInvoiceServiceNotFoundException

		service = (
			await self.draft_purchase_invoice_servicetype_service.get_services_by_id(
				draft_invoice.fk_invoice_service
			)
		)

		if not service:
			raise DraftPurchaseInvoiceServiceNotFoundException

		# Validar archivos en storage (capa de aplicación)
		if draft_invoice.id_receipt_file:
			receipt_file_metadata = await self._get_metadata_or_none(
				draft_invoice.id_receipt_file
			)
			if not receipt_file_metadata:
				raise DraftPurchaseInvoiceReceiptFileInvalidException

		if service.require_detail_file and draft_invoice.id_details_file:
			detail_file_metadata = await self._get_metadata_or_none(
				draft_invoice.id_details_file
			)
			if not detail_file_metadata:
				raise DraftPurchaseInvoiceDetailFileInvalidException

		# Validar campos obligatorios (capa de dominio)
		await self.draft_purchase_invoice_usecase.validate_draft_purchase_invoice(
			draft_invoice, service
		)

		# Marcar como "Finalized"
		finalized_draft = (
			await self.draft_purchase_invoice_usecase.finalize_draft_purchase_invoice(
				draft_invoice
			)
		)

		# Crear PurchaseInvoice desde el draft
		new_purchase_invoice = {
			"fk_provider": finalized_draft.fk_provider,
			"fk_service": finalized_draft.fk_invoice_service,
			"number": finalized_draft.number,
			"concept": finalized_draft.concept,
			"issue_date": finalized_draft.issue_date,
			"receipt_date": finalized_draft.receipt_date,
			"service_month": finalized_draft.service_month,
			"currency": finalized_draft.currency,
			"unit_price": finalized_draft.unit_price,
			"air_waybill": finalized_draft.awb,
			"kilograms": finalized_draft.kg,
			"items": finalized_draft.items,
			"fk_receipt_file": finalized_draft.id_receipt_file,
			"fk_detail_file": finalized_draft.id_details_file,
		}

		purchase_invoice = await self.purchase_invoice_service().create(
			new_purchase_invoice
		)
		purchase_invoice_created = await self.purchase_invoice_service().save_and_emit(
			purchase_invoice
		)

		# Vincular factura con draft
		finalized_draft.fk_invoice = purchase_invoice_created.id
		await self.save_draft_purchase_invoice(finalized_draft)

		return purchase_invoice_created

	async def _get_metadata_or_none(self, file_id: uuid.UUID | None):
		if not file_id:
			return None
		try:
			metadata = await self.file_storage_service().get_metadata(file_id)
			return metadata
		except Exception as e:
			print("Hubo un error al obtener la metadata:", e)
			return None
