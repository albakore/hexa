from datetime import date
import uuid
from sqlmodel import SQLModel, Field


class DraftPurchaseInvoice(SQLModel, table=True):
	id: int | None = Field(None, primary_key=True)
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
	state: str | None = Field(default=None, description="Estado de la factura en draft")

	id_receipt_file: uuid.UUID | None = Field(
		default=None, description="Archivo de comprobante"
	)
	id_details_file: uuid.UUID | None = Field(
		default=None, description="Archivo de detalle"
	)
