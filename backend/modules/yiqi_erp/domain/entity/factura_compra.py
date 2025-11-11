from typing import Optional
from datetime import date
from pydantic import Field

from modules.yiqi_erp.domain.entity.entity_base import YiqiEntity


class FacturaDeCompra(YiqiEntity):
	__internal_name__ = "FACTURA_COMPRA"
	__prefix__ = "FACO"

	ESTADO_DE_VENCIMIENT: Optional[str] = Field(
		default=None, serialization_alias="6382"
	)
	CANTIDAD_DE_DIAS_VEN: Optional[int] = Field(
		default=None, serialization_alias="6381"
	)
	ESTADO_VENCIMIENTO: Optional[str] = Field(default=None, serialization_alias="6383")
	TOTAL_1V: Optional[float] = Field(default=None, serialization_alias="2884")
	IVA_USD: Optional[float] = Field(default=None, serialization_alias="7185")
	PENDIENTE_PAGO: Optional[float] = Field(default=None, serialization_alias="4076")
	PENDIEN_USD: Optional[float] = Field(default=None, serialization_alias="6509")
	SALDO: Optional[float] = Field(default=None, serialization_alias="4077")
	SALDO_USD: Optional[float] = Field(default=None, serialization_alias="6214")
	TIPO_DE_CAMBIO_AL_PA: Optional[float] = Field(
		default=None, serialization_alias="5077"
	)
	USD: Optional[float] = Field(default=None, serialization_alias="5131")
	COSTO_PROMEDIO_POR_K: Optional[float] = Field(
		default=None, serialization_alias="6601"
	)
	COSTO_PROMEDIO_POR_I: Optional[float] = Field(
		default=None, serialization_alias="6602"
	)
	TOTAL_A_PAGAR: Optional[float] = Field(default=None, serialization_alias="6969")
	CLIE_ID_PROV: Optional[int] = Field(default=None, serialization_alias="2880")
	ID_FACTURA: Optional[int] = Field(default=None, serialization_alias="6638")
	TIFA_ID_TIFA: Optional[int] = Field(default=None, serialization_alias="2878")
	NUMERO: Optional[str] = Field(default=None, serialization_alias="2879")
	SUCU_ID_SUCU: Optional[int] = Field(default=None, serialization_alias="5406")
	CONCEPTO: Optional[str] = Field(default=None, serialization_alias="2888")
	ARHC_ID_2736: Optional[int] = Field(default=None, serialization_alias="2891")
	AWB: Optional[str] = Field(default=None, serialization_alias="7102")
	DETALLE_ADJ: Optional[int] = Field(default=None, serialization_alias="5494")
	SERV_ID_SERV: Optional[int] = Field(default=None, serialization_alias="6196")
	LINK: Optional[str] = Field(default=None, serialization_alias="7015")
	AO_DE_BALANCE: Optional[date] = Field(default=None, serialization_alias="6488")
	MARCA_DE_FACTURADO: Optional[bool] = Field(default=None, serialization_alias="6958")
	RETENCIONES_APLICADA: Optional[bool] = Field(
		default=None, serialization_alias="7050"
	)
	MARCA_TC: Optional[bool] = Field(default=None, serialization_alias="6557")
	SECT_ID_DEPA: Optional[int] = Field(default=None, serialization_alias="6558")
	BANC_ID_BANC: Optional[int] = Field(default=None, serialization_alias="6564")
	FECHA_EMISION: Optional[date] = Field(default=None, serialization_alias="2881")
	FECHA_DE_RECEPCION: Optional[date] = Field(default=None, serialization_alias="5112")
	MES_DE_SERVICIO: Optional[date] = Field(default=None, serialization_alias="5082")
	FECHA_PERIODO_DESDE: Optional[date] = Field(
		default=None, serialization_alias="2889"
	)
	FECHA_PERIODO_HASTA: Optional[date] = Field(
		default=None, serialization_alias="2890"
	)
	AJUSTE_DE_NC: Optional[float] = Field(default=None, serialization_alias="6204")
	PRECIO_UNITARIO: Optional[float] = Field(default=None, serialization_alias="6405")
	NETO_DE_CONTROLADOR: Optional[float] = Field(
		default=None, serialization_alias="6475"
	)
	MONE_ID_MONE: Optional[int] = Field(default=None, serialization_alias="5074")
	TIPO_DE_CAMBIO: Optional[str] = Field(default=None, serialization_alias="6629")
	TC_FACO: Optional[str] = Field(default=None, serialization_alias="7105")
	MARCA_DE_GASTOS: Optional[bool] = Field(default=None, serialization_alias="6402")
	CUCO_ID_CUGA: Optional[int] = Field(default=None, serialization_alias="3209")
	MONE_ID_MON1: Optional[int] = Field(default=None, serialization_alias="5076")
	FECHA_DE_TC_AL_PAGO: Optional[date] = Field(
		default=None, serialization_alias="5078"
	)
	MONE_ID_MON2: Optional[int] = Field(default=None, serialization_alias="5081")
	MOMO_ID_MOTI: Optional[int] = Field(default=None, serialization_alias="6466")
	MOTIVO_DE_ANULACION: Optional[str] = Field(default=None, serialization_alias="6617")
	ESRE_ID_ESRE: Optional[int] = Field(default=None, serialization_alias="7101")
	OBJECIONES_DE_TARIFA: Optional[str] = Field(
		default=None, serialization_alias="5481"
	)
	ADJUNTO_TARIFA: Optional[int] = Field(default=None, serialization_alias="6449")
	OBJECIONES_DE_VOLUME: Optional[str] = Field(
		default=None, serialization_alias="5479"
	)
	ADJUNTO_VOLUMEN: Optional[int] = Field(default=None, serialization_alias="6448")
	ENTRADA_CONTROL_VOLU: Optional[date] = Field(
		default=None, serialization_alias="5483"
	)
	ENTRADA_CONTROL_TARI: Optional[date] = Field(
		default=None, serialization_alias="5484"
	)
	ENTRADA_CONTROL_ADM: Optional[date] = Field(
		default=None, serialization_alias="5485"
	)
	ENTRADA_A_MODIF_PEDI: Optional[date] = Field(
		default=None, serialization_alias="5538"
	)
	RESPONSABLE_ADM: Optional[int] = Field(default=None, serialization_alias="6231")
	RESPONSABLE_CONTROL_: Optional[int] = Field(
		default=None, serialization_alias="6230"
	)
	RESPON_TARIF: Optional[int] = Field(default=None, serialization_alias="6506")
	EMPL_ID_EMPL: Optional[int] = Field(default=None, serialization_alias="6634")
	KG: Optional[float] = Field(default=None, serialization_alias="6599")
	ITEMS: Optional[int] = Field(default=None, serialization_alias="6600")
	FECHA_DE_PAGO: Optional[date] = Field(default=None, serialization_alias="5534")
	FECHA_DE_DETALLES_SO: Optional[date] = Field(
		default=None, serialization_alias="6906"
	)
	IMPU_ID_IMPU: Optional[int] = Field(default=None, serialization_alias="6951")
	IMPU_ID_IMP2: Optional[int] = Field(default=None, serialization_alias="6954")
	CORE_ID_CORE: Optional[int] = Field(default=None, serialization_alias="6952")
	CORE_ID_CON2: Optional[int] = Field(default=None, serialization_alias="6955")
	IMPORTE_RETENCION_1: Optional[float] = Field(
		default=None, serialization_alias="6953"
	)
	IMPUESTO_RETENCION_2: Optional[float] = Field(
		default=None, serialization_alias="6956"
	)
	CAMPO_TEST: Optional[str] = Field(default=None, serialization_alias="7060")
	ID_URUGUAY: Optional[int] = Field(default=None, serialization_alias="7092")
	MARCA_TRACKING: Optional[str] = None
	PUNTO_DE_VENTA: Optional[int] = Field(default=None, serialization_alias="5423")
	PAIS_DEL_PROVEEDOR: Optional[str] = Field(default=None, serialization_alias="5098")
	TRATADA_OBJ_TARIFA: Optional[bool] = Field(default=None, serialization_alias="5482")
	TRATADA_OBJ_VOLUMEN: Optional[bool] = Field(
		default=None, serialization_alias="5480"
	)
	INICIO_DE_CONTROL: Optional[date] = Field(default=None, serialization_alias="5061")
	PEDIDO_DE_CAMBIO_INT: Optional[date] = Field(
		default=None, serialization_alias="5062"
	)
	PEDIDO_DE_CAMBIO_AL_: Optional[date] = Field(
		default=None, serialization_alias="5063"
	)
	ACEPTACION: Optional[date] = Field(default=None, serialization_alias="5064")
	LIQI_ID_LIQI: Optional[int] = Field(default=None, serialization_alias="3189")
	ENTRADA_A_CONTROL_RE: Optional[date] = Field(
		default=None, serialization_alias="5489"
	)
	CLIE_ID_CLIE: Optional[int] = Field(default=None, serialization_alias="3284")
	PROY_ID_PROY: Optional[int] = Field(default=None, serialization_alias="3285")
	ORCO_ID_ORCO: Optional[int] = Field(default=None, serialization_alias="3357")
	TOTAL_2V: Optional[float] = Field(default=None, serialization_alias="2885")
	TOTAL_AJUSTADO: Optional[float] = Field(default=None, serialization_alias="5290")
	OBJECIONES_CONTROL_A: Optional[str] = Field(
		default=None, serialization_alias="6503"
	)
	TRATADA_OBJ_ADM: Optional[bool] = Field(default=None, serialization_alias="6504")
	ADJUNTO_ADM: Optional[int] = Field(default=None, serialization_alias="6505")
	SALDO_AJUSTADO_PROVE: Optional[float] = Field(
		default=None, serialization_alias="6247"
	)
	FECHA_2V: Optional[date] = Field(default=None, serialization_alias="2887")
	PUVE_ID_PUVE: Optional[int] = Field(default=None, serialization_alias="5404")
	CAJA_ID_CAJA: Optional[int] = Field(default=None, serialization_alias="5227")
	OBLI_ID_OBLI: Optional[int] = Field(default=None, serialization_alias="2893")
	NETO_PROYECTADO: Optional[float] = Field(default=None, serialization_alias="5380")
	IVA_PROYECTADO: Optional[float] = Field(default=None, serialization_alias="5385")
	TOTAL_PROYECTADO: Optional[float] = Field(default=None, serialization_alias="5386")
	FECHA_EMISION_PROYEC: Optional[date] = Field(
		default=None, serialization_alias="5387"
	)
	TIPO_DE_CAMBIO_ORIGI: Optional[float] = Field(
		default=None, serialization_alias="5075"
	)
	ID_PREVISION: Optional[str] = Field(default=None, serialization_alias="7179")
	ASIE_ID_ASIE: Optional[int] = Field(default=None, serialization_alias="3149")
	AUDI_USUA_ALTA: Optional[str] = None
	AUDI_FECHA_ALTA: Optional[date] = None
	AUDI_USUA_MODIF: Optional[str] = None
	AUDI_FECHA_MODIF: Optional[date] = None
	ESTADO_DE_EMPRESA: Optional[str] = Field(default=None, serialization_alias="6755")
	REGION: Optional[str] = Field(default=None, serialization_alias="6654")
	PAIS: Optional[str] = Field(default=None, serialization_alias="7226")
	COMENTARIOS: Optional[str] = Field(default=None, serialization_alias="7016")
	FECHA_1V: Optional[date] = Field(default=None, serialization_alias="2886")
	NETO: Optional[float] = Field(default=None, serialization_alias="2882")
	IVA: Optional[float] = Field(default=None, serialization_alias="2883")
	TOTAL_NOTA_DE_CREDIT: Optional[float] = Field(
		default=None, serialization_alias="5291"
	)
	USD_NC: Optional[float] = Field(default=None, serialization_alias="6189")
	NRO_COMPLETO: Optional[str] = Field(default=None, serialization_alias="5422")
	USD_AL_PAGO: Optional[float] = Field(default=None, serialization_alias="6978")
	CANCELACION: Optional[float] = Field(default=None, serialization_alias="7107")
	CANCELACION_USD: Optional[float] = Field(default=None, serialization_alias="6981")
	CANCELACIONES_EN_PRO: Optional[float] = Field(
		default=None, serialization_alias="7229"
	)
	ENTRADA_RECIBIDA: Optional[date] = Field(default=None, serialization_alias="6535")
	FECHA_ULTIMO_PAGO: Optional[date] = Field(default=None, serialization_alias="6528")
	TIEMPO_EN_C_VOLUMEN: Optional[str] = Field(default=None, serialization_alias="5486")
	TIEMPO_EN_C_TARIFA: Optional[str] = Field(default=None, serialization_alias="5487")
	TIEMPO_EN_C_ADM: Optional[str] = Field(default=None, serialization_alias="5488")
	DIAS_EN_C_VOLUMEN: Optional[int] = Field(default=None, serialization_alias="5535")
	DIAS_EN_C_TARIFAS: Optional[int] = Field(default=None, serialization_alias="5536")
	DIAS_EN_C_ADM: Optional[int] = Field(default=None, serialization_alias="5537")
	DIAS_EN_MODIF_PEDIDA: Optional[int] = Field(
		default=None, serialization_alias="5539"
	)
	DIAS_HASTA_PAGADA: Optional[int] = Field(default=None, serialization_alias="5543")
	TOTAL_RETENCIONES: Optional[float] = Field(default=None, serialization_alias="6959")
	PROV_NOMBRE: Optional[str] = None
	CPAS_RS_RNI: Optional[int] = Field(default=None, serialization_alias="3822")
	PERCEPCIONES_IVA: Optional[float] = Field(default=None, serialization_alias="3812")
	PERCEPCIONES_IIBB: Optional[float] = Field(default=None, serialization_alias="3811")
	PERCEPCIONES_IG: Optional[float] = Field(default=None, serialization_alias="3816")
	IVA_27: Optional[float] = Field(default=None, serialization_alias="4519")
	IVA_21: Optional[float] = Field(default=None, serialization_alias="4518")
	IVA_105: Optional[float] = Field(default=None, serialization_alias="4517")
	TOTAL_GRAVADO: Optional[float] = Field(default=None, serialization_alias="3813")
	TOTAL_NO_GRAVADO: Optional[float] = Field(default=None, serialization_alias="3814")
	TOTAL_EXENTO: Optional[float] = Field(default=None, serialization_alias="4520")
	TOTAL_SUSS_OTROS: Optional[float] = Field(default=None, serialization_alias="3815")
	DIAS_EN_CONTROL_REAL: Optional[int] = Field(
		default=None, serialization_alias="6390"
	)
	TOTAL_NOTA_DE_DEBITO: Optional[float] = Field(
		default=None, serialization_alias="5292"
	)
	TOTAL_PERCEPCIONES: Optional[float] = Field(
		default=None, serialization_alias="3146"
	)
	SALDO_AJUSTADO: Optional[float] = Field(default=None, serialization_alias="6261")
	FCDF_ID_FCDF: Optional[int] = Field(default=None, serialization_alias="6729")
	FECHA_REAL_DE_PAGO: Optional[date] = Field(default=None, serialization_alias="6442")
	KEY_FACO_CLIE: Optional[str] = Field(default=None, serialization_alias="7084")
	ESTA_CODIGO: Optional[int] = None
	DESC_ESTADO: Optional[str] = None
