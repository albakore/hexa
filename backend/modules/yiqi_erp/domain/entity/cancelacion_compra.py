from typing import Optional
from datetime import date, datetime

from modules.yiqi_erp.domain.entity.entity_base import YiqiEntity


class CancelacionDeCompras(YiqiEntity):
	__internal_name__ = "CANCELACION_DE_COMPR"
	__prefix__ = "CADC"

	CLIE_ID_CLIE: Optional[int] = None
	OBLI_ID_OBLI: Optional[int] = None
	FACO_ID_FACO: Optional[int] = None
	MONTO: Optional[float] = None
	MONE_ID_MONE: Optional[int] = None
	TC_AL_DIA_DE_PAGO: Optional[float] = None
	COMENTARIOS: Optional[str] = None
	ID_URUGUAY: Optional[int] = None
	AUDI_USUA_ALTA: Optional[str] = None
	AUDI_FECHA_ALTA: Optional[date] = None
	AUDI_USUA_MODIF: Optional[str] = None
	AUDI_FECHA_MODIF: Optional[date] = None
	ID_DE_FACTURA: Optional[str] = None
	FORMULA_FACTURA: Optional[str] = None
	ESTADO_DE_FACTURA: Optional[str] = None
	SUCU_ID_SUCU: Optional[int] = None
	MONEDA_DE_PAGO: Optional[str] = None
	TC_TRANSFERENCIA: Optional[float] = None
	ID_CANCELACION: Optional[int] = None
	MONTO_X_TC: Optional[float] = None
	CANTIDAD_DE_DIAS_VEN: Optional[int] = None
	FECHA_1: Optional[date] = None
	OP_FECHA_PAGO: Optional[date] = None
	IMPORTE_CANCELADO: Optional[float] = None
	TIPO_DE_CAMBIO_FACTU: Optional[str] = None
	IMPORTE_A_CANCELAR_U: Optional[float] = None
	SERVICIO_FACO: Optional[str] = None
	ESTA_CODIGO: Optional[int] = None
	DESC_ESTADO: Optional[str] = None
