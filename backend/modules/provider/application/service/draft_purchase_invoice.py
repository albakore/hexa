from dataclasses import dataclass
from io import BytesIO
from typing import Sequence
import uuid

from dependency_injector.providers import Factory
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
from modules.yiqi_erp.application.service.yiqi import YiqiService
from modules.yiqi_erp.domain.command import CreateYiqiInvoiceCommand, UploadFileCommand


@dataclass
class DraftPurchaseInvoiceService:
	draft_purchase_invoice_repository: DraftPurchaseInvoiceRepository
	file_storage_service: type
	yiqi_service: YiqiService
	currency_service: type | None

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

	async def finalize_and_emit_invoice(self, id_draft_purchase_invoice: int):
		draft_invoice = await self.get_draft_purchase_invoice_by_id(
			id_draft_purchase_invoice
		)
		invoice_with_metadata = await self.get_draft_purchase_invoice_with_filemetadata(
			draft_invoice
		)
		if not draft_invoice.currency:
			raise DraftPurchaseInvoiceCurrencyNotFoundException
		yiqi_currency = await self.yiqi_service.get_currency_by_code(
			draft_invoice.currency, 316
		)

		comprobante = invoice_with_metadata.receipt_file
		detalle = invoice_with_metadata.details_file

		yiqi_comprobante = None
		yiqi_detalle = None

		if comprobante:
			archivo_comprobante = await self.file_storage_service().download_file(
				comprobante.id
			)
			yiqi_comprobante = UploadFileCommand(
				BytesIO(archivo_comprobante.file),
				size=comprobante.size,
				filename=comprobante.download_filename,
			)
			await self.yiqi_service.upload_file(yiqi_comprobante, 316)

		if detalle:
			archivo_detalle = await self.file_storage_service().download_file(
				detalle.id
			)
			yiqi_detalle = UploadFileCommand(
				BytesIO(archivo_detalle.file),
				size=detalle.size,
				filename=detalle.download_filename,
			)

			await self.yiqi_service.upload_file(yiqi_detalle, 316)

		yiqi_invoice_command = CreateYiqiInvoiceCommand(
			Provider=draft_invoice.fk_provider,
			Numero=draft_invoice.number,
			Concepto=draft_invoice.concept or "Sin concepto agregado",
			Servicio=draft_invoice.fk_invoice_service,
			Moneda_original=yiqi_currency["id"],
			Precio_unitario=draft_invoice.unit_price or 0.0,
			Mes_servicio=draft_invoice.service_month,
			Comprobante=yiqi_comprobante,
			Detalle=yiqi_detalle,
			Fecha_emision=draft_invoice.issue_date,
			Fecha_recepcion=draft_invoice.receipt_date,
			AWB=draft_invoice.awb,
			Items=draft_invoice.items,
			Kg=draft_invoice.kg,
			creado_en_portal=True,
		)

		yiqi_invoice = await self.yiqi_service.create_invoice(yiqi_invoice_command, 316)
		draft_invoice.state = "Created"
		await self.save_draft_purchase_invoice(draft_invoice)
		return yiqi_invoice

	async def _get_metadata_or_none(self, file_id: uuid.UUID | None):
		if not file_id:
			return None
		try:
			metadata = await self.file_storage_service().get_metadata(file_id)
			return metadata
		except Exception as e:
			print("Hubo un error al obtener la metadata:", e)
			return None
