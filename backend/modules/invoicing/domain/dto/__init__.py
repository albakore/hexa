from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class DraftInvoiceCreateDTO(BaseModel):
	numero: str
	concepto: Optional[str] = None
	awb: Optional[str] = None

	precio_unitario: Optional[float] = None
	kg: Optional[float] = None
	items: Optional[int] = None

	fecha_emision: Optional[datetime] = None
	fecha_recepcion: Optional[datetime] = None

	fk_proveedor: Optional[int] = None
	fk_servicio: Optional[int] = None
	fk_moneda: Optional[int] = None
	fk_invoice: Optional[int] = None
