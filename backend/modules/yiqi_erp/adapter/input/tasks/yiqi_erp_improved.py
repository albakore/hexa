"""
Improved Tasks del módulo YiqiERP - Input Adapter.

Mejoras sobre la versión original:
1. Uso del nuevo CreateYiqiInvoiceCommand con validaciones completas
2. Mejor manejo de errores con mensajes claros
3. Validación temprana de datos
4. Logging estructurado
5. Type hints más precisos
"""

import logging
import uuid
from decimal import Decimal
from io import BytesIO
from typing import Any, Dict

from core.config.settings import env
from core.db.session import reset_session_context, set_session_context
from modules.yiqi_erp.container import YiqiContainer
from modules.yiqi_erp.domain.command.improved_commands import (
	CreateYiqiInvoiceCommand,
	UploadFileCommand,
)
from shared.interfaces.service_locator import service_locator
from shared.interfaces.service_protocols import (
	FileStorageServiceProtocol,
	ProviderServiceProtocol,
	PurchaseInvoiceServiceProtocol,
	PurchaseInvoiceServiceTypeServiceProtocol,
)

# Configure logger
logger = logging.getLogger(__name__)


class InvoiceCreationError(Exception):
	"""Custom exception for invoice creation errors."""

	def __init__(self, message: str, details: Dict[str, Any] | None = None):
		self.message = message
		self.details = details or {}
		super().__init__(self.message)


async def create_invoice_from_purchase_invoice_improved_tasks(
	purchase_invoice_id: int, schema_id: int = env.YIQI_SCHEMA
) -> Dict[str, Any]:
	"""
	Task mejorada para crear factura en YiqiERP desde una PurchaseInvoice.

	Mejoras sobre la versión original:
	- Validación temprana con Pydantic v2
	- Mejor manejo de errores
	- Logging estructurado
	- Mensajes de error claros

	Args:
	    purchase_invoice_id: ID de la purchase invoice
	    schema_id: ID de la compañía (default desde env)

	Returns:
	    Dict con la respuesta de YiqiERP incluyendo newId

	Raises:
	    InvoiceCreationError: Si hay problemas en la creación
	    ValueError: Si los datos son inválidos

	Example:
	    >>> result = await create_invoice_from_purchase_invoice_tasks(
	    ...     purchase_invoice_id=123,
	    ...     schema_id=316
	    ... )
	    >>> print(result['newId'])
	    456
	"""

	logger.info(
		f"Starting invoice creation for purchase_invoice_id={purchase_invoice_id}, "
		f"schema_id={schema_id}"
	)

	# Initialize services
	yiqi_service = YiqiContainer().service()
	session_uuid = uuid.uuid4()
	context = set_session_context(str(session_uuid))

	try:
		# === Step 1: Get required services ===
		logger.debug("Getting required services from service locator")

		provider_service: ProviderServiceProtocol = service_locator.get_service(
			"provider_service"
		)
		purchase_invoice_service: PurchaseInvoiceServiceProtocol = (
			service_locator.get_service("purchase_invoice_service")
		)
		servicetype_service: PurchaseInvoiceServiceTypeServiceProtocol = (
			service_locator.get_service("draft_invoice_servicetype_service")
		)
		file_storage_service: FileStorageServiceProtocol = service_locator.get_service(
			"file_storage_service"
		)

		# === Step 2: Fetch invoice and related data ===
		logger.debug(f"Fetching purchase invoice {purchase_invoice_id}")

		purchase_invoice = await purchase_invoice_service.get_one_by_id(
			purchase_invoice_id
		)

		if not purchase_invoice:
			raise InvoiceCreationError(
				f"Purchase invoice not found: {purchase_invoice_id}",
				{"purchase_invoice_id": purchase_invoice_id},
			)

		logger.info(
			f"Found invoice: number={purchase_invoice.number}, "
			f"provider_id={purchase_invoice.fk_provider}"
		)

		# === Step 3: Validate required foreign keys ===
		if not purchase_invoice.fk_provider:
			raise InvoiceCreationError(
				"Invoice missing required provider",
				{"purchase_invoice_id": purchase_invoice_id, "field": "fk_provider"},
			)

		if not purchase_invoice.fk_service:
			raise InvoiceCreationError(
				"Invoice missing required service",
				{"purchase_invoice_id": purchase_invoice_id, "field": "fk_service"},
			)

		# === Step 4: Fetch related entities ===
		logger.debug("Fetching provider and service data")

		provider = await provider_service.get_provider_by_id(
			purchase_invoice.fk_provider
		)

		if not provider:
			raise InvoiceCreationError(
				f"Provider not found: {purchase_invoice.fk_provider}",
				{"provider_id": purchase_invoice.fk_provider},
			)

		if not provider.id_yiqi_provider:
			raise InvoiceCreationError(
				f"Provider missing Yiqi ID: {provider.id}",
				{
					"provider_id": provider.id,
					"provider_name": getattr(provider, "name", "N/A"),
				},
			)

		service = await servicetype_service.get_services_by_id(
			purchase_invoice.fk_service
		)

		if not service:
			raise InvoiceCreationError(
				f"Service not found: {purchase_invoice.fk_service}",
				{"service_id": purchase_invoice.fk_service},
			)

		if not service.id_yiqi_service:
			raise InvoiceCreationError(
				f"Service missing Yiqi ID: {service.id}",
				{
					"service_id": service.id,
					"service_name": getattr(service, "name", "N/A"),
				},
			)

		# === Step 5: Get currency ===
		logger.debug(f"Fetching currency: {purchase_invoice.currency}")

		yiqi_currency = await yiqi_service.get_currency_by_code(
			purchase_invoice.currency, schema_id
		)

		if not yiqi_currency or "id" not in yiqi_currency:
			raise InvoiceCreationError(
				f"Currency not found in Yiqi: {purchase_invoice.currency}",
				{"currency_code": purchase_invoice.currency, "schema_id": schema_id},
			)

		# === Step 6: Process file attachments ===
		yiqi_comprobante = None
		yiqi_detalle = None

		if purchase_invoice.fk_receipt_file:
			logger.debug(f"Processing receipt file: {purchase_invoice.fk_receipt_file}")

			try:
				comprobante_metadata = await file_storage_service.get_metadata(
					purchase_invoice.fk_receipt_file
				)
				archivo_comprobante = await file_storage_service.download_file(
					purchase_invoice.fk_receipt_file
				)

				# Create upload command with validation
				yiqi_comprobante = UploadFileCommand(
					file=BytesIO(archivo_comprobante.file),
					size=comprobante_metadata.size,
					filename=comprobante_metadata.download_filename,
				)

				await yiqi_service.upload_file(yiqi_comprobante, schema_id)
				logger.info(
					f"Receipt file uploaded: {comprobante_metadata.download_filename}"
				)

			except ValueError as e:
				raise InvoiceCreationError(
					f"Invalid receipt file: {str(e)}",
					{
						"file_id": str(purchase_invoice.fk_receipt_file),
						"validation_error": str(e),
					},
				)
			except Exception as e:
				raise InvoiceCreationError(
					f"Failed to upload receipt file: {str(e)}",
					{"file_id": str(purchase_invoice.fk_receipt_file)},
				)

		if purchase_invoice.fk_detail_file:
			logger.debug(f"Processing detail file: {purchase_invoice.fk_detail_file}")

			try:
				detalle_metadata = await file_storage_service.get_metadata(
					purchase_invoice.fk_detail_file
				)
				archivo_detalle = await file_storage_service.download_file(
					purchase_invoice.fk_detail_file
				)

				# Create upload command with validation
				yiqi_detalle = UploadFileCommand(
					file=BytesIO(archivo_detalle.file),
					size=detalle_metadata.size,
					filename=detalle_metadata.download_filename,
				)

				await yiqi_service.upload_file(yiqi_detalle, schema_id)
				logger.info(
					f"Detail file uploaded: {detalle_metadata.download_filename}"
				)

			except ValueError as e:
				raise InvoiceCreationError(
					f"Invalid detail file: {str(e)}",
					{
						"file_id": str(purchase_invoice.fk_detail_file),
						"validation_error": str(e),
					},
				)
			except Exception as e:
				raise InvoiceCreationError(
					f"Failed to upload detail file: {str(e)}",
					{"file_id": str(purchase_invoice.fk_detail_file)},
				)

		# === Step 7: Create invoice command with full validation ===
		logger.debug("Creating invoice command with validation")

		try:
			# Prepare data for command
			command_data = {
				"Provider": provider.id_yiqi_provider,
				"Servicio": service.id_yiqi_service,
				"Numero": purchase_invoice.number,
				"Concepto": purchase_invoice.concept,
				"Fecha_emision": purchase_invoice.issue_date,
				"Fecha_recepcion": purchase_invoice.receipt_date,
				"Mes_servicio": purchase_invoice.service_month,
				"Precio_unitario": Decimal(str(purchase_invoice.unit_price)),
				"Moneda_original": yiqi_currency["id"],
				"creado_en_portal": True,
			}

			# Add optional fields
			if purchase_invoice.air_waybill:
				command_data["AWB"] = purchase_invoice.air_waybill

			if purchase_invoice.kilograms is not None:
				command_data["Kg"] = float(purchase_invoice.kilograms)

			if purchase_invoice.items is not None:
				command_data["Items"] = purchase_invoice.items

			if yiqi_comprobante:
				command_data["Comprobante"] = yiqi_comprobante

			if yiqi_detalle:
				command_data["Detalle"] = yiqi_detalle

			# Create command - Pydantic v2 will validate everything!
			yiqi_invoice = CreateYiqiInvoiceCommand(**command_data)

			logger.info(
				f"Invoice command created successfully. "
				f"Computed fields: days_to_reception={yiqi_invoice.days_to_reception}, "
				f"avg_weight_per_item={yiqi_invoice.average_weight_per_item}"
			)

		except ValueError as e:
			# Pydantic validation error - provide clear message
			raise InvoiceCreationError(
				f"Invoice data validation failed: {str(e)}",
				{
					"purchase_invoice_id": purchase_invoice_id,
					"validation_error": str(e),
					"invoice_number": purchase_invoice.number,
				},
			)

		# === Step 8: Create invoice in Yiqi ===
		logger.info(
			f"Creating invoice in Yiqi for invoice number: {purchase_invoice.number}"
		)

		try:
			yiqi_response = await yiqi_service.create_invoice(yiqi_invoice, schema_id)

			if "newId" not in yiqi_response:
				raise InvoiceCreationError(
					"Yiqi response missing 'newId'", {"response": yiqi_response}
				)

			logger.info(
				f"Invoice created successfully in Yiqi. "
				f"Yiqi ID: {yiqi_response['newId']}"
			)

		except Exception as e:
			raise InvoiceCreationError(
				f"Failed to create invoice in Yiqi: {str(e)}",
				{
					"purchase_invoice_id": purchase_invoice_id,
					"invoice_number": purchase_invoice.number,
				},
			)

		# === Step 9: Update purchase invoice with Yiqi ID ===
		logger.debug(
			f"Updating purchase invoice with Yiqi ID: {yiqi_response['newId']}"
		)

		try:
			purchase_invoice.fk_yiqi_invoice = yiqi_response.get("newId")
			await purchase_invoice_service.save(purchase_invoice)

			logger.info(
				f"Purchase invoice updated successfully. "
				f"ID: {purchase_invoice_id}, Yiqi ID: {purchase_invoice.fk_yiqi_invoice}"
			)

		except Exception as e:
			# Log warning but don't fail - invoice was created in Yiqi
			logger.warning(
				f"Failed to update purchase invoice with Yiqi ID: {str(e)}",
				extra={
					"purchase_invoice_id": purchase_invoice_id,
					"yiqi_invoice_id": yiqi_response.get("newId"),
				},
			)

		return yiqi_response

	except InvoiceCreationError:
		# Re-raise our custom errors as-is
		raise

	except Exception as e:
		# Catch any unexpected errors
		logger.exception(
			f"Unexpected error creating invoice for purchase_invoice_id={purchase_invoice_id}"
		)
		raise InvoiceCreationError(
			f"Unexpected error: {str(e)}",
			{
				"purchase_invoice_id": purchase_invoice_id,
				"error_type": type(e).__name__,
			},
		)

	finally:
		# Always reset session context
		reset_session_context(context)
		logger.debug(f"Session context reset: {session_uuid}")


# === Helper function for testing/debugging ===


async def validate_invoice_before_creation(
	purchase_invoice_id: int, schema_id: int = env.YIQI_SCHEMA
) -> Dict[str, Any]:
	"""
	Validate invoice data without creating it.

	Useful for pre-flight checks in UI or testing.

	Args:
	    purchase_invoice_id: ID de la purchase invoice
	    schema_id: ID de la compañía

	Returns:
	    Dict con el resultado de validación:
	    {
	        "valid": bool,
	        "errors": List[str],
	        "warnings": List[str],
	        "invoice_data": Dict
	    }
	"""
	errors = []
	warnings = []

	try:
		# Get services
		purchase_invoice_service: PurchaseInvoiceServiceProtocol = (
			service_locator.get_service("purchase_invoice_service")
		)

		# Get invoice
		purchase_invoice = await purchase_invoice_service.get_one_by_id(
			purchase_invoice_id
		)

		if not purchase_invoice:
			errors.append(f"Invoice not found: {purchase_invoice_id}")
			return {"valid": False, "errors": errors, "warnings": warnings}

		# Check required fields
		if not purchase_invoice.fk_provider:
			errors.append("Missing provider")

		if not purchase_invoice.fk_service:
			errors.append("Missing service")

		if not purchase_invoice.number:
			errors.append("Missing invoice number")

		# Try creating command to validate
		try:
			command_data = {
				"Provider": purchase_invoice.fk_provider or 0,
				"Servicio": purchase_invoice.fk_service,
				"Numero": purchase_invoice.number or "MISSING",
				"Concepto": purchase_invoice.concept or "MISSING",
				"Fecha_emision": purchase_invoice.issue_date,
				"Fecha_recepcion": purchase_invoice.receipt_date,
				"Mes_servicio": purchase_invoice.service_month,
				"Precio_unitario": Decimal(str(purchase_invoice.unit_price or 0)),
				"Moneda_original": 1,  # Dummy value
			}

			CreateYiqiInvoiceCommand(**command_data)

		except ValueError as e:
			errors.append(f"Validation error: {str(e)}")

		# Warnings
		if not purchase_invoice.fk_receipt_file:
			warnings.append("No receipt file attached")

		if not purchase_invoice.air_waybill:
			warnings.append("No AWB specified")

		return {
			"valid": len(errors) == 0,
			"errors": errors,
			"warnings": warnings,
			"invoice_data": {
				"id": purchase_invoice.id,
				"number": purchase_invoice.number,
				"provider_id": purchase_invoice.fk_provider,
				"service_id": purchase_invoice.fk_service,
			},
		}

	except Exception as e:
		errors.append(f"Validation failed: {str(e)}")
		return {"valid": False, "errors": errors, "warnings": warnings}
