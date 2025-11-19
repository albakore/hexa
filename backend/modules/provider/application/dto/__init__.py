from datetime import date

from pydantic import BaseModel
from sqlmodel import Field

from modules.file_storage.domain.entity import FileMetadata
from modules.provider.domain.entity.purchase_invoice_service import (
	PurchaseInvoiceService,
)


class DraftPurchaseInvoiceDTO(BaseModel):
	id: int | None = None
	number: str | None = Field(default=None, description="Numero de la factura")
	concept: str | None = Field(default=None, description="Concepto")
	fk_provider: int | None = Field(default=None, description="ID de proveedor")
	fk_invoice_service: int | None = Field(
		default=None, description="ID servicio de factura"
	)

	service_month: date | None = Field(default=None, description="Mes del servicio")
	awb: str | None = Field(default=None, description="Air Waybill (Guia aerea)")
	kg: float | None = Field(default=None, description="Peso del paquete")
	items: int | None = Field(default=None, description="Cantidad de items")
	unit_price: float | None = Field(default=None, description="Precio unitario")
	currency: str | None = Field(default=None, description="EL tipo de moneda")

	issue_date: date | None = Field(default=None, description="Fecha de emision")
	receipt_date: date | None = Field(default=None, description="Fecha de recepcion")

	fk_invoice: int | None = Field(default=None, description="ID de factura creada")

	receipt_file: FileMetadata | None = Field(
		default=None, description="Archivo de comprobante"
	)
	details_file: FileMetadata | None = Field(
		default=None, description="Archivo de detalle"
	)


class ProviderServiceWithRequirementsDTO(BaseModel):
	"""DTO que combina los datos del servicio con los requerimientos de la tabla intermedia"""

	# Datos del servicio
	id: int | None = None
	name: str
	description: str | None = None
	group: str | None = None
	id_yiqi_service: int | None = None

	# Requerimientos de la tabla intermedia (ProviderInvoiceServiceLink)
	require_awb: bool | None = None
	require_unit_price: bool | None = None
	require_kg: bool | None = None
	require_items: bool | None = None
	require_detail_file: bool | None = None
