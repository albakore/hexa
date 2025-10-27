from dataclasses import dataclass
from io import BytesIO
from shared.interfaces.service_locator import ServiceLocator
from shared.interfaces.service_protocols import (
	YiqiServiceProtocol,
	PurchaseInvoiceServiceProtocol,
	FileStorageServiceProtocol,
)
from modules.yiqi_erp.domain.command import CreateYiqiInvoiceCommand, UploadFileCommand


@dataclass
class InvoiceIntegrationService:
	yiqi_service: YiqiServiceProtocol

	async def create_invoice_from_purchase_invoice(
		self, purchase_invoice_id: int, company_id: int = 316
	):
		service_locator = ServiceLocator()
		purchase_invoice_service: PurchaseInvoiceServiceProtocol = (
			service_locator.get_service("invoicing.purchase_invoice_service")
		)
		file_storage_service: FileStorageServiceProtocol = service_locator.get_service(
			"file_storage.file_storage_service"
		)

		purchase_invoice = await purchase_invoice_service.get_one_by_id(
			purchase_invoice_id
		)
		yiqi_currency = await self.yiqi_service.get_currency_by_code(
			purchase_invoice.currency, company_id
		)

		yiqi_comprobante = None
		yiqi_detalle = None

		if purchase_invoice.fk_receipt_file:
			comprobante_metadata = await file_storage_service.get_metadata(
				purchase_invoice.fk_receipt_file
			)
			archivo_comprobante = await file_storage_service.download_file(
				purchase_invoice.fk_receipt_file
			)
			yiqi_comprobante = UploadFileCommand(
				BytesIO(archivo_comprobante.file),
				size=comprobante_metadata.size,
				filename=comprobante_metadata.download_filename,
			)
			await self.yiqi_service.upload_file(yiqi_comprobante, company_id)

		if purchase_invoice.fk_detail_file:
			detalle_metadata = await file_storage_service.get_metadata(
				purchase_invoice.fk_detail_file
			)
			archivo_detalle = await file_storage_service.download_file(
				purchase_invoice.fk_detail_file
			)
			yiqi_detalle = UploadFileCommand(
				BytesIO(archivo_detalle.file),
				size=detalle_metadata.size,
				filename=detalle_metadata.download_filename,
			)
			await self.yiqi_service.upload_file(yiqi_detalle, company_id)

		yiqi_invoice_command = CreateYiqiInvoiceCommand(
			Provider=purchase_invoice.fk_provider,
			Numero=purchase_invoice.number,
			Concepto=purchase_invoice.concept or "Sin concepto agregado",
			Servicio=purchase_invoice.fk_service,
			Moneda_original=yiqi_currency["id"],
			Precio_unitario=purchase_invoice.unit_price or 0.0,
			Mes_servicio=purchase_invoice.service_month,
			Comprobante=yiqi_comprobante,
			Detalle=yiqi_detalle,
			Fecha_emision=purchase_invoice.issue_date,
			Fecha_recepcion=purchase_invoice.receipt_date,
			AWB=purchase_invoice.air_waybill,
			Items=purchase_invoice.items,
			Kg=purchase_invoice.kilograms,
			creado_en_portal=True,
		)

		yiqi_invoice = await self.yiqi_service.create_invoice(
			yiqi_invoice_command, company_id
		)

		purchase_invoice.fk_yiqi_invoice = yiqi_invoice.get("id")
		await purchase_invoice_service.save(purchase_invoice)

		return yiqi_invoice
