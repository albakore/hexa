"""
Tasks del módulo YiqiERP - Input Adapter.

Estas funciones se registrarán automáticamente como tasks de Celery
a través del service_locator y el discovery automático.

NOTA: Las funciones async son soportadas automáticamente.
El sistema las envuelve en un wrapper síncrono usando asyncio.run().
"""

from io import BytesIO
import uuid
import pandas as pd
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
from core.config.settings import env
from shared.interfaces.service_protocols.provider import AirWaybillServiceProtocol


async def create_invoice_from_purchase_invoice_tasks(
	purchase_invoice_id: int, schema_id: int = env.YIQI_SCHEMA
):
	"""
	Task para crear factura en YiqiERP desde una PurchaseInvoice.

	Esta función async será envuelta automáticamente en un wrapper síncrono
	para ser compatible con Celery.

	Será registrada automáticamente como: "yiqi_erp.create_invoice_from_purchase_invoice_tasks"

	Args:
		purchase_invoice_id: ID de la purchase invoice
		schema_id: ID de la compañía (default: 316)

	Returns:
		Respuesta del servicio YiqiERP
	"""
	try:
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
		air_waybill_service: AirWaybillServiceProtocol = service_locator.get_service(
			"air_waybill_service"
		)
		file_storage_service: FileStorageServiceProtocol = service_locator.get_service(
			"file_storage_service"
		)
		purchase_invoice = await purchase_invoice_service.get_one_by_id(
			purchase_invoice_id
		)
		if not purchase_invoice:
			raise Exception(
				f"La purchase invoice con ID {purchase_invoice_id} no existe."
			)
		provider = await provider_service.get_provider_by_id(
			purchase_invoice.fk_provider
		)
		if not provider:
			raise Exception(
				f"El proveedor con ID {purchase_invoice.fk_provider} no existe."
			)
		service = await draft_purchase_invoice_servicetype_service.get_services_by_id(
			purchase_invoice.fk_service
		)
		if not service:
			raise Exception(
				f"El servicio con ID {purchase_invoice.fk_service} no existe."
			)
		yiqi_currency = await yiqi_service.get_currency_by_code(
			purchase_invoice.currency, schema_id
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
			await yiqi_service.upload_file(yiqi_comprobante, schema_id)

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
			await yiqi_service.upload_file(yiqi_detalle, schema_id)

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

		yiqi_response = await yiqi_service.create_invoice(yiqi_invoice, schema_id)
		yiqi_request_is_ok = yiqi_response.get("ok")
		if not yiqi_request_is_ok:
			raise Exception(
				f"Error al crear la factura en YiqiERP: {yiqi_response.get('error')}"
			)
		purchase_invoice.fk_yiqi_invoice = yiqi_response.get("newId")
		purchase_invoice.invoice_status = "SENT"
		await purchase_invoice_service.save(purchase_invoice)
		print(yiqi_response)

		air_waybills = (
			await air_waybill_service.get_air_waybills_by_purchase_invoice_id(
				purchase_invoice.id
			)
		)
		columns = [
			"🔑 Proveedor (Nombre)",
			"🔑 Factura (Id factura)",
			"🔑 Guía aérea",
			"CN38",
			"Origen (País)",
			"Destino (País)",
			"Kg",
			"Bags",
		]
		rows = [
			(
				"CLIE_ID_CLIE",
				"FACO_ID_FACO",
				"GUAE_GUIA_AEREA",
				"GUAE_CN38",
				"PAIS_ID_PAI1",
				"PAIS_ID_PAIS",
				"GUAE_KG",
				"GUAE_BAGS",
			)
		]
		for item in air_waybills:
			rows.append(
				(
					str(provider.id_yiqi_provider),
					str(purchase_invoice.fk_yiqi_invoice),
					item.awb_code,
					"",
					item.origin,
					item.destination,
					str(item.kg),
					"",
				)
			)
		df = pd.DataFrame(rows, columns=columns)
		print(df)
		buffer = BytesIO()
		df.to_excel(buffer, index=False, engine="openpyxl")
		buffer.seek(0)
		yiqi_awb_bytes = buffer.getvalue()

		yiqi_awb_file = UploadFileCommand(
			BytesIO(yiqi_awb_bytes),
			size=len(yiqi_awb_bytes),
			filename="air_waybills.xlsx",
		)
		buffer.close()

		yiqi_awb_creation = await yiqi_service.create_multiple_air_waybills(
			yiqi_awb_file, schema_id
		)
		print(yiqi_awb_creation)
		if not yiqi_awb_creation:
			raise Exception(
				f"Error al crear la(s) guía(s) aérea(s) en YiqiERP: {yiqi_response.get('error')}"
			)

		if not purchase_invoice.fk_yiqi_invoice:
			raise Exception(
				"La purchase invoice no tiene fk_yiqi_invoice asignado, no se pueden consultar las AWBs en Yiqi."
			)
		yiqi_awbs = await yiqi_service.get_air_waybills_by_invoice_id(
			purchase_invoice.fk_yiqi_invoice, schema_id
		)

		for awb in yiqi_awbs:
			for air_waybill in air_waybills:
				if awb.get("GUAE_GUIA_AEREA") == air_waybill.awb_code:
					air_waybill.fk_yiqi_awb = awb.get("id")
					await air_waybill_service.save_air_waybill(air_waybill)
					break

		return yiqi_response
	finally:
		reset_session_context(context)
