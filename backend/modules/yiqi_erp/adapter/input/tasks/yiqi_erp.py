"""
Tasks del módulo YiqiERP - Input Adapter.

Estas funciones se registrarán automáticamente como tasks de Celery
a través del service_locator y el discovery automático.

NOTA: Las funciones async son soportadas automáticamente.
El sistema las envuelve en un wrapper síncrono usando asyncio.run().
"""

from io import BytesIO
import uuid
from shared.interfaces.service_locator import service_locator
from shared.interfaces.service_protocols import (
	FileStorageServiceProtocol,
	ProviderServiceProtocol,
	PurchaseInvoiceServiceProtocol,
	PurchaseInvoiceServiceTypeServiceProtocol,
)
from modules.yiqi_erp.container import YiqiContainer
from modules.yiqi_erp.domain.command import CreateYiqiInvoiceCommand, UploadFileCommand
from core.db.session import set_session_context, reset_session_context


async def create_invoice_from_purchase_invoice_tasks(
	purchase_invoice_id: int, company_id: int = 316
):
	"""
	Task para crear factura en YiqiERP desde una PurchaseInvoice.

	Esta función async será envuelta automáticamente en un wrapper síncrono
	para ser compatible con Celery.

	Será registrada automáticamente como: "yiqi_erp.create_invoice_from_purchase_invoice_tasks"

	Args:
		purchase_invoice_id: ID de la purchase invoice
		company_id: ID de la compañía (default: 316)

	Returns:
		Respuesta del servicio YiqiERP
	"""

	yiqi_service = YiqiContainer().service()

	session_uuid = uuid.uuid4()
	context = set_session_context(str(session_uuid))

	provider_service: ProviderServiceProtocol = service_locator.get_service(
		"provider_service"
	)
	purchase_invoice_service: PurchaseInvoiceServiceProtocol = (
		service_locator.get_service("purchase_invoice_service")
	)
	draft_purchase_invoice_servicetype_service: PurchaseInvoiceServiceTypeServiceProtocol = service_locator.get_service(
		"draft_invoice_servicetype_service"
	)
	file_storage_service: FileStorageServiceProtocol = service_locator.get_service(
		"file_storage_service"
	)
	purchase_invoice = await purchase_invoice_service.get_one_by_id(purchase_invoice_id)
	provider = await provider_service.get_provider_by_id(purchase_invoice.fk_provider)
	service = await draft_purchase_invoice_servicetype_service.get_services_by_id(
		purchase_invoice.fk_service
	)
	yiqi_currency = await yiqi_service.get_currency_by_code(
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
		await yiqi_service.upload_file(yiqi_comprobante, company_id)

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
		await yiqi_service.upload_file(yiqi_detalle, company_id)

	yiqi_invoice = CreateYiqiInvoiceCommand(
		Provider=provider.id_yiqi_provider,
		Servicio=service.id_yiqi_service,
		Numero=purchase_invoice.number,
		Concepto=purchase_invoice.concept,
		Fecha_emision=purchase_invoice.issue_date,
		Fecha_recepcion=purchase_invoice.receipt_date,
		AWB=purchase_invoice.air_waybill,
		Moneda_original=yiqi_currency["id"],
		Precio_unitario=purchase_invoice.unit_price,
		Mes_servicio=purchase_invoice.service_month,
		Items=purchase_invoice.items,
		Kg=purchase_invoice.kilograms,
		creado_en_portal=True,
		Comprobante=yiqi_comprobante,
		Detalle=yiqi_detalle,
	)

	yiqi_response = await yiqi_service.create_invoice(yiqi_invoice, company_id)
	purchase_invoice.fk_yiqi_invoice = yiqi_response.get("newId")
	await purchase_invoice_service.save(purchase_invoice)
	reset_session_context(context)
	print(yiqi_response)
	return yiqi_response
