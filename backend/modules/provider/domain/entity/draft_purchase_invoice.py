from datetime import date, datetime
import uuid
from sqlmodel import SQLModel, Relationship, Field

class DraftPurchaseInvoice(SQLModel, table=True):
	id : int | None = Field(None, primary_key=True)
	numero : str = Field(default=None, description="Numero de la factura")
	concepto : str | None = Field(default=None, description="Concepto")
	fk_proveedor : int | None = Field(default=None, )
	fk_servicio : int | None = Field(default=None,)
	moneda : str | None = Field(default=None, description="EL tipo de moneda")

	awb : str | None = Field(default=None)

	precio_unitario : float | None = Field(default=None)
	kg : float | None = Field(default=None)
	items : int | None = Field(default=None)

	fecha_emision : date | None = Field(default=None, description="Fecha de emision")
	fecha_recepcion : date | None = Field(default=None, description="Fecha de recepcion")

	fk_invoice : int | None = Field(default=None)

	id_archivo_comprobante : uuid.UUID | None = Field(default=None)
	id_archivo_detalle : uuid.UUID | None = Field(default=None)