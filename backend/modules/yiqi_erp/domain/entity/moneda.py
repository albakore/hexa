from typing import Optional
from datetime import date, datetime, time
from pydantic import BaseModel

from modules.yiqi_erp.domain.entity.entity_base import YiqiEntity

class Moneda(YiqiEntity):
	__internal_name__ = "MONEDA"
	__prefix__ = "MONE"

	NOMBRE: Optional[str]
	PAIS_ID_PAIS: Optional[int]
	CODIGO_AFIP: Optional[str]
	CAMBIO_ULTIMO_DIAS_D: Optional[float]
	CAMBIO_ULTIMO_DIA_DE: Optional[str]
	ID_URUGUAY: Optional[int]
	ULTIMA_FECHA: Optional[date]
	AUDI_USUA_ALTA: Optional[str]
	AUDI_FECHA_ALTA: Optional[date]
	AUDI_USUA_MODIF: Optional[str]
	AUDI_FECHA_MODIF: Optional[date]
	ESTA_CODIGO: Optional[int]
	DESC_ESTADO: Optional[str]


