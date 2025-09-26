from typing import Optional
from datetime import date

from modules.yiqi_erp.domain.entity.entity_base import YiqiEntity


class NotaCreditoVenta(YiqiEntity):
	__internal_name__ = "NOTA_CREDITO"
	__prefix__ = "NOCR"

	CLIE_ID_CLIE: Optional[int] = None
	FACT_ID_FACT: Optional[int] = None
	PUVE_ID_PUVE: Optional[int] = None
	TIFA_ID_TIFA: Optional[int] = None
	NUMERO: Optional[int] = None
	PRSE_ID_PRSE: Optional[int] = None
	COVE_ID_COVE: Optional[int] = None
	OBSERVACIONES: Optional[str] = None
	FECHA_EMISION: Optional[date] = None
	FECHA_VENCIMIENTO: Optional[date] = None
	FECHA_PERIODO_DESDE: Optional[date] = None
	FECHA_PERIODO_HASTA: Optional[date] = None
	MES_DE_SERVICIO: Optional[date] = None
	ARHC_ID_3621: Optional[int] = None
	MONEDA_RESULTADO: Optional[int] = None
	MONE_ID_MON1: Optional[int] = None
	COTIZACION: Optional[int] = None
	OBJECIONES_DE_VOLUME: Optional[str] = None
	TRATADA_OBJ_VOLUMEN: Optional[bool] = None
	OBJECIONES_DE_TARIFA: Optional[str] = None
	TRATADA_OBJ_TARIFA: Optional[bool] = None
	RECALCULO_REALIZADO: Optional[bool] = None
	INGRESO_CONTROL_VOLU: Optional[date] = None
	INGRESO_CONTROL_TARI: Optional[date] = None
	ASIE_ID_ASIE: Optional[int] = None
	LIQI_ID_LIQI: Optional[int] = None
	CPAS_RS_RNI: Optional[int] = None
	RET_IVA: Optional[int] = None
	RET_IIBB: Optional[int] = None
	RET_IG: Optional[int] = None
	SUSS_Y_OTROS: Optional[int] = None
	IMPUESTOS_INTERNO: Optional[int] = None
	IMPUESTOS_MUNICIP: Optional[int] = None
	CAE: Optional[str] = None
	CAE_VENCIMIENTO: Optional[str] = None
	CANT_DETALLES: Optional[str] = None
	ERROR_AFIP: Optional[str] = None
	MONE_ID_MONE: Optional[int] = None
	IDENTIFICADOR_NC: Optional[int] = None
	AUDI_USUA_ALTA: Optional[str] = None
	AUDI_FECHA_ALTA: Optional[date] = None
	AUDI_USUA_MODIF: Optional[str] = None
	AUDI_FECHA_MODIF: Optional[date] = None
	NETO: Optional[int] = None
	IVA: Optional[int] = None
	TOTAL: Optional[int] = None
	USD: Optional[int] = None
	MONEDA_TC_NC: Optional[int] = None
	RESPONSABLE_CONTROL_: Optional[str] = None
	RESPONSABLE_CONT_TA: Optional[str] = None
	DIAS_EN_CONTROL_VOLU: Optional[int] = None
	DIAS_EN_CONTROL_TARI: Optional[int] = None
	IVA_27: Optional[int] = None
	IVA_21: Optional[int] = None
	IVA_105: Optional[int] = None
	TOTAL_GRAVADO: Optional[int] = None
	TOTAL_NO_GRAVADO: Optional[int] = None
	TOTAL_EXENTO: Optional[int] = None
	ESTA_CODIGO: Optional[int] = None
	DESC_ESTADO: Optional[str] = None
