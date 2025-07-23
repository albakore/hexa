from typing import Optional
from datetime import date

from modules.yiqi_erp.domain.entity.entity_base import YiqiEntity

class NotaCreditoCompra(YiqiEntity):
	__internal_name__ = "NOTA_CREDITO_COMPRA"
	__prefix__ = "NOCC"

	TIFA_ID_TIFA: Optional[int] = None
	NUMERO: Optional[str] = None
	FECHA_DE_EMISION: Optional[date] = None
	CLIE_ID_CLIE: Optional[int] = None
	FACO_ID_FACO: Optional[int] = None
	MONC_ID_MONC: Optional[int] = None
	OBSERVACIONES: Optional[str] = None
	COMPROBANTE_NC: Optional[int] = None
	DETALLE: Optional[int] = None
	ITEMS: Optional[int] = None
	ASIE_ID_ASIE: Optional[int] = None
	MONE_ID_MONE: Optional[int] = None
	TC_NC: Optional[str] = None
	CONCEPTO: Optional[str] = None
	AO_BALANCE: Optional[int] = None
	PRECIO_UNITARIO: Optional[int] = None
	CANTIDAD: Optional[int] = None
	ID_URUGUAY: Optional[int] = None
	LIQI_ID_LIQI: Optional[int] = None
	TIPO_DE_CAMBIO_ORIGI: Optional[int] = None
	MONE_ID_MON1: Optional[int] = None
	TIPO_DE_CAMBIO_AL_PA: Optional[int] = None
	FECHA_DE_TC_AL_PAGO: Optional[date] = None
	MONE_ID_MON2: Optional[int] = None
	PAIS_DEL_PROVEEDOR: Optional[str] = None
	TIPO_CAMBIO: Optional[int] = None
	AUDI_USUA_ALTA: Optional[str] = None
	AUDI_FECHA_ALTA: Optional[date] = None
	AUDI_USUA_MODIF: Optional[str] = None
	AUDI_FECHA_MODIF: Optional[date] = None
	ESTADO_FACTURA: Optional[str] = None
	NETO: Optional[int] = None
	TOTAL: Optional[int] = None
	DESCRIPCION: Optional[str] = None
	NETO_TC: Optional[int] = None
	ID_NOTA_CREDITO: Optional[int] = None
	USD: Optional[int] = None
	IVA: Optional[int] = None
	PERCEP_IIBB_CABA: Optional[int] = None
	PERCEP_IIBB_BSAS: Optional[int] = None
	PERCEP_IIBB_TOTAL: Optional[int] = None
	PERCEPCIONES_IVA: Optional[int] = None
	PERCEPCIONES_TOTAL: Optional[int] = None
	IVA_27: Optional[int] = None
	IVA_21: Optional[int] = None
	IVA_105: Optional[int] = None
	TOTAL_GRAVADO: Optional[int] = None
	TOTAN_NO_GRAVADO: Optional[int] = None
	TOTAL_EXENTO: Optional[int] = None
	ESTA_CODIGO: Optional[int] = None
	DESC_ESTADO: Optional[str] = None


class OrdenDePago(YiqiEntity):
	__internal_name__ = "ORDEN_PAGO"
	__prefix__ = "OBLI"

	ID_ORDEN_DE_PAGO: Optional[int] = None
	NUMERO: Optional[int] = None
	CLIE_ID_CLIE: Optional[int] = None
	SALDO_PROVEEDOR: Optional[int] = None
	CONT_ID_CONT: Optional[int] = None
	AVISAR_A_TODOS_LOS_C: Optional[bool] = None
	DESCRIPCION: Optional[str] = None
	FECHAESPERADA: Optional[date] = None
	COMPROBANTE_DE_PAGO_: Optional[int] = None
	DE_SALDO_PREVIO: Optional[int] = None
	A_CUENTA: Optional[int] = None
	ACLARACIONES: Optional[str] = None
	CUDE_ID_CUDE: Optional[int] = None
	SUCU_ID_SUCU: Optional[int] = None
	SALDO_PROVEEDOR_A_AP: Optional[int] = None
	MONE_ID_PROV: Optional[int] = None
	MONE_ID_MONE: Optional[int] = None
	TC_OP: Optional[str] = None
	FONDEO: Optional[int] = None
	ADJUNTAR_RECLAMO: Optional[int] = None
	ADJUNTO: Optional[int] = None
	COMENTARIOS: Optional[str] = None
	USD_CANCELACIONES: Optional[int] = None
	CUCO_ID_CUCO: Optional[int] = None
	ASIE_ID_ASIE: Optional[int] = None
	RETENCIONES_APLICADA: Optional[int] = None
	INSTRUCCIONES: Optional[str] = None
	CHEQ_ID_CHEQ: Optional[int] = None
	TC_AL_DIA_DE_PAGO: Optional[int] = None
	AUDI_USUA_ALTA: Optional[str] = None
	AUDI_FECHA_ALTA: Optional[date] = None
	AUDI_USUA_MODIF: Optional[str] = None
	AUDI_FECHA_MODIF: Optional[date] = None
	EMPL_ID_EMPL: Optional[int] = None
	MONTO: Optional[int] = None
	PENDIENTE_CANCELACIO: Optional[int] = None
	TOTAL_ASIGNADO: Optional[int] = None
	DIAS_A_FECHA_DE_PAGO: Optional[int] = None
	TOTAL_CANCELACIONES: Optional[int] = None
	TOTA_TXS: Optional[int] = None
	ORIGEN___BANCO_MLA: Optional[str] = None
	CUDE_ID_BENE: Optional[int] = None
	SALDO_PROVEEDOR_A_US: Optional[int] = None
