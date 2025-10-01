from datetime import date, datetime
from typing import Any, Dict

from pydantic import BaseModel

from shared.file_storage.domain.entity import FileMetadata


class DraftPurchaseInvoiceDTO(BaseModel):
	id: int | None
	numero: str
	concepto: str | None
	fk_proveedor: int | None
	fk_servicio: int | None
	moneda: str | None
	awb: str | None
	precio_unitario: float | None
	kg: float | None
	items: int | None
	fecha_emision: date | None
	fecha_recepcion: date | None

	archivo_comprobante: FileMetadata | None
	archivo_detalle: FileMetadata | None
