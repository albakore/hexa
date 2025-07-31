from datetime import datetime
import uuid
from pydantic import BaseModel, Field

class CreateProviderCommand(BaseModel):
	name : str = Field(...,description="Name of provider")
	id_yiqi_provider : int | None = Field(default=None,description="Id of yiqi provider")

class UpdateProviderCommand(BaseModel):
	id : int
	name : str = Field(...,description="Name of provider")
	id_yiqi_provider : int | None = Field(default=None,description="Id of yiqi provider")

class CreateDraftPurchaseInvoiceCommand(BaseModel):
	numero : str
	concepto : str | None = None
	fk_proveedor : int | None = None
	fk_servicio : int | None = None
	fk_moneda : int | None = None
	awb : str | None = None
	precio_unitario : float | None = None
	kg : float | None = None
	items : int | None = None
	fecha_emision : datetime | None = None
	fecha_recepcion : datetime | None = None
	id_archivo_comprobante : uuid.UUID | None = None
	id_archivo_detalle : uuid.UUID | None = None