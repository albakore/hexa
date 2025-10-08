from datetime import date, datetime
import uuid
from pydantic import BaseModel, Field


class CreateProviderCommand(BaseModel):
	name: str = Field(..., description="Name of provider")
	id_yiqi_provider: int | None = Field(
		default=None, description="Id of yiqi provider"
	)


class UpdateProviderCommand(BaseModel):
	id: int
	name: str = Field(..., description="Name of provider")
	id_yiqi_provider: int | None = Field(
		default=None, description="Id of yiqi provider"
	)


class CreateDraftPurchaseInvoiceCommand(BaseModel):
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

	id_receipt_file: uuid.UUID | None = Field(
		default=None, description="Archivo de comprobante"
	)
	id_details_file: uuid.UUID | None = Field(
		default=None, description="Archivo de detalle"
	)


###
### INVOICE SERVICE
###
class CreatePurchaseInvoiceServiceCommand(BaseModel):
	name: str
	description: str | None = None
	group: str | None = None
	require_awb: bool | None = None
	require_unit_price: bool | None = None
	require_kg: bool | None = None
	require_items: bool | None = None
	require_detail_file: bool | None = None
	id_yiqi_service: int | None = None


class UpdateDraftPurchaseInvoiceCommand(CreateDraftPurchaseInvoiceCommand): ...


class UpdatePurchaseInvoiceServiceCommand(CreatePurchaseInvoiceServiceCommand):
	id: int
	id_yiqi_service: int | None = Field(default=None, description="Id of yiqi provider")
