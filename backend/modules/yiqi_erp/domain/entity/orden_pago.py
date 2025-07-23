from typing import Optional
from datetime import date, datetime

from modules.yiqi_erp.domain.entity.entity_base import YiqiEntity

class OrdenDePago(YiqiEntity):
	__internal_name__ = "ORDEN_PAGO"
	__prefix__ = "OBLI"

	ID_ORDEN_DE_PAGO: Optional[int] = None
	NUMERO: Optional[int] = None
	CLIE_ID_CLIE: Optional[int] = None
	SALDO_PROVEEDOR: Optional[float] = None
	CONT_ID_CONT: Optional[int] = None
	AVISAR_A_TODOS_LOS_C: Optional[bool] = None
	DESCRIPCION: Optional[str] = None
	FECHAESPERADA: Optional[date] = None
	COMPROBANTE_DE_PAGO_: Optional[int] = None
	DE_SALDO_PREVIO: Optional[float] = None
	A_CUENTA: Optional[float] = None
	ACLARACIONES: Optional[str] = None
	CUDE_ID_CUDE: Optional[int] = None
	SUCU_ID_SUCU: Optional[int] = None
	SALDO_PROVEEDOR_A_AP: Optional[float] = None
	MONE_ID_PROV: Optional[int] = None
	MONE_ID_MONE: Optional[int] = None
	TC_OP: Optional[str] = None
	FONDEO: Optional[float] = None
	ADJUNTAR_RECLAMO: Optional[int] = None
	ADJUNTO: Optional[int] = None
	COMENTARIOS: Optional[str] = None
	USD_CANCELACIONES: Optional[float] = None
	CUCO_ID_CUCO: Optional[int] = None
	ASIE_ID_ASIE: Optional[int] = None
	RETENCIONES_APLICADA: Optional[float] = None
	INSTRUCCIONES: Optional[str] = None
	CHEQ_ID_CHEQ: Optional[int] = None
	TC_AL_DIA_DE_PAGO: Optional[float] = None
	AUDI_USUA_ALTA: Optional[str] = None
	AUDI_FECHA_ALTA: Optional[date] = None
	AUDI_USUA_MODIF: Optional[str] = None
	AUDI_FECHA_MODIF: Optional[date] = None
	EMPL_ID_EMPL: Optional[int] = None
	MONTO: Optional[float] = None
	PENDIENTE_CANCELACIO: Optional[float] = None
	TOTAL_ASIGNADO: Optional[float] = None
	DIAS_A_FECHA_DE_PAGO: Optional[int] = None
	TOTAL_CANCELACIONES: Optional[float] = None
	TOTA_TXS: Optional[int] = None
	ORIGEN___BANCO_MLA: Optional[str] = None
	CUDE_ID_BENE: Optional[int] = None
	SALDO_PROVEEDOR_A_US: Optional[float] = None
	ESTIMADO_IMPORTE_MON: Optional[float] = None
	TOTAL_A_TRANSFERIR_M: Optional[float] = None
	TOTAL_TXS: Optional[int] = None
	TOTAL_CHEQUES: Optional[int] = None
	TOTAL_CHEQUES_3: Optional[int] = None
	CHEQUES_A_DEBITAR: Optional[int] = None
	TOTAL_EFECTIVO: Optional[float] = None
	TOTAL_DEBITOS: Optional[float] = None
	TOTAL_RETENCIONES: Optional[float] = None
	DESCRIPCION_AUTOMATI: Optional[str] = None
	TOTAL_TARJETA: Optional[float] = None
	ESTA_CODIGO: Optional[int] = None
	DESC_ESTADO: Optional[str] = None