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
	numero: str
	concepto: str | None = None
	fk_proveedor: int | None = None
	fk_servicio: int | None = None
	moneda: str | None = None
	awb: str | None = None
	precio_unitario: float | None = None
	kg: float | None = None
	items: int | None = None
	fecha_emision: date | None = None
	fecha_recepcion: date | None = None
	id_archivo_comprobante: uuid.UUID | None = None
	id_archivo_detalle: uuid.UUID | None = None


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
