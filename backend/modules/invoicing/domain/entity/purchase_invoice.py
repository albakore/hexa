from datetime import date
import uuid
from sqlmodel import SQLModel, Field
from shared.mixins import AuditMixin, TimestampMixin


class PurchaseInvoice(SQLModel, AuditMixin, TimestampMixin, table=True):
	# region General
	# General

	# Id factura | ID_FACTURA
	id: int | None = Field(default=None, primary_key=True)

	# Número | NUMERO
	number: str | None = Field(default=None)

	# Tipo de factura | TIFA_ID_TIFA
	invoice_type: str | None = Field(default=None)

	# Proveedor | CLIE_ID_PROV
	fk_provider: int | None = Field(default=None)

	# Estado de empresa | ESTADO_DE_EMPRESA
	# company_status: str

	# Sucursal | SUCU_ID_SUCU
	branch: str | None = Field(default=None)

	# Región | REGION
	region: str | None = Field(default=None)

	# Descripción | DESCRIPCION
	description: str | None = Field(default=None)

	# Concepto | CONCEPTO
	concept: str | None = Field(default=None)

	# Comprobante | ARHC_ID_2736
	fk_receipt_file: uuid.UUID | None = Field(default=None)

	# AWB | AWB
	air_waybill: str | None = Field(default=None)

	# Detalle | DETALLE_ADJ
	fk_detail_file: uuid.UUID | None = Field(default=None)

	# Servicio | SERV_ID_SERV
	fk_service: int | None

	# Pais | PAIS
	country: str | None = Field(default=None)

	# Link | LINK
	link_url_file: str | None = Field(default=None)

	# Continente | CONTINENTE
	continent: str | None = Field(default=None)

	# Año de balance | AO_DE_BALANCE
	balance_year: str | None = Field(default=None)

	# Marca de pagado | MARCA_DE_FACTURADO
	paid: bool | None = Field(default=None)

	# Marca de gastos | MARCA_DE_GASTOS
	expense_mark: bool | None = Field(default=None)

	# Retenciones aplicadas | RETENCIONES_APLICADA
	applied_retentions: bool | None = Field(default=None)

	# Agentes Independientes | AGENTES_INDEPENDIENT
	independent_agents: str | None = Field(default=None)

	# Estado de la factura (Interno)
	invoice_status: str | None = Field(default=None)

	# TC | TC
	# tc: str

	# Marca TC | MARCA_TC
	# marca_tc: str

	# Sector | SECT_ID_DEPA
	# sector: str

	# Banco Titular | BANC_ID_BANC
	# banco_titular: str

	# region Fechas
	# Fechas | SEPA_FECHAS

	# Fecha de emisión | FECHA_EMISION
	issue_date: date | None = Field(default=None)

	# Fecha de Recepción | FECHA_DE_RECEPCION
	receipt_date: date | None = Field(default=None)

	# Mes de servicio | MES_DE_SERVICIO
	service_month: date | None = Field(default=None)

	# Fecha período desde | FECHA_PERIODO_DESDE
	period_from_date: date | None = Field(default=None)

	# Fecha período hasta | FECHA_PERIODO_HASTA
	period_until_date: date | None = Field(default=None)

	# 1er. venc. | FECHA_1V
	first_expiration_Date: date | None = Field(default=None)

	# Estado de vencimiento | ESTADO_DE_VENCIMIENT
	# estado_vencimiento_color: str

	# Cantidad de días vencimiento | CANTIDAD_DE_DIAS_VEN
	# dias_vencimiento: str

	# Estado vencimiento | ESTADO_VENCIMIENTO
	# estado_vencimiento: str

	# region Montos
	# Montos | SEPA_MONTOS

	# # Neto | NETO
	# name: str

	# # IVA | IVA
	# name: str

	# # Neto IVA | TOTAL_1V
	# name: str

	# # IVA USD | IVA_USD
	# name: str

	# # Total NCs | TOTAL_NOTA_DE_CREDIT
	# name: str

	# # USD NC | USD_NC
	# name: str

	# # Pendiente de Cancelación | PENDIENTE_PAGO
	# name: str

	# # Pendientes de cancelacion USD | PENDIEN_USD
	# name: str

	# # Saldo | SALDO
	# name: str

	# # Saldo USD | SALDO_USD
	# name: str

	# # Ajuste NC | AJUSTE_DE_NC
	# name: str

	# Precio unitario | PRECIO_UNITARIO
	unit_price: float | None = Field(default=None)

	# # Neto de controlador | NETO_DE_CONTROLADOR
	# name: str

	# # Monedas | MONEDAS
	# name: str

	# # Moneda original | MONE_ID_MONE
	# fk_currency: str
	currency: str | None = Field(default=None)

	# # TC FACO | TC_FACO
	# name: str

	# # Pago | PAGO
	# name: str

	# # Cuenta de Gastos | CUCO_ID_CUGA
	# name: str

	# # Moneda de pago | MONE_ID_MON1
	# name: str

	# # Tipo de cambio al pago | TIPO_DE_CAMBIO_AL_PA
	# name: str

	# # Fecha de TC al pago | FECHA_DE_TC_AL_PAGO
	# name: str

	# # Moneda TC original | MONE_ID_MON2
	# name: str

	# # USD | USD
	# name: str

	# # nro completo | NRO_COMPLETO
	# name: str

	# # USD al pago | USD_AL_PAGO
	# name: str

	# # Cancelacion | CANCELACION
	# name: str

	# # Cancelacion USD | CANCELACION_USD
	# name: str

	# # Cancelaciones en proceso | CANCELACIONES_EN_PRO
	# name: str

	# # Motivos | MOTIVOS
	# name: str

	# # Motivo de envío a modificaciones pedidas | MOMO_ID_MOTI
	# name: str

	# # Motivo de Anulación | MOAN_ID_MOAN
	# name: str

	# # Estado reclamo | ESRE_ID_ESRE
	# name: str

	# # Fechas de Control | TIEMPOS_SEP
	# name: str

	# # Entrada Control Volumen | ENTRADA_CONTROL_VOLU
	# name: str

	# # Entrada Control Tarifa | ENTRADA_CONTROL_TARI
	# name: str

	# # Entrada Control ADM | ENTRADA_CONTROL_ADM
	# name: str

	# # Entrada a Modif. Pedidas | ENTRADA_A_MODIF_PEDI
	# name: str

	# # Entrada Recibida | ENTRADA_RECIBIDA
	# name: str

	# # Semáforos Control | SEM_SEP
	# name: str

	# # Fecha último Pago | FECHA_ULTIMO_PAGO
	# name: str

	# # Tiempo en C. Volumen | TIEMPO_EN_C_VOLUMEN
	# name: str

	# # Tiempo en C. Tarifa | TIEMPO_EN_C_TARIFA
	# name: str

	# # Tiempo en C. ADM | TIEMPO_EN_C_ADM
	# name: str

	# # Días Control | DIAS_SEP
	# name: str

	# # Días en C. Volumen | DIAS_EN_C_VOLUMEN
	# name: str

	# # Días en C. Tarifas | DIAS_EN_C_TARIFAS
	# name: str

	# # Días en C. ADM | DIAS_EN_C_ADM
	# name: str

	# # Días en Modif. Pedidas | DIAS_EN_MODIF_PEDIDA
	# name: str

	# # Dias hasta Pagada | DIAS_HASTA_PAGADA
	# name: str

	# # Responsables | RESP_SEP
	# name: str

	# # responsable ADM | RESPONSABLE_ADM
	# name: str

	# # Responsable control volumen | RESPONSABLE_CONTROL_
	# name: str

	# # Responsable control tarifa | RESPON_TARIF
	# name: str

	# # Responsable cuenta | EMPL_ID_EMPL
	# name: str

	# # Gerente | GERENTE
	# name: str

	# # Costo promedio | COSTO_PROMEDIO
	# name: str

	# # Kg | KG
	kilograms: float | None = Field(default=None)

	# # Costo promedio por Kg | COSTO_PROMEDIO_POR_K
	# name: str

	# # Items | ITEMS
	items: int | None = Field(default=None)

	# # Costo promedio por Item | COSTO_PROMEDIO_POR_I
	# name: str

	# # Fecha estado pagada | FECHA_DE_PAGO
	# name: str

	# # Fecha de detalles solicitados | FECHA_DE_DETALLES_SO
	# name: str

	# # Kg AWB Total | KG_AWB_TOTAL
	# name: str

	# # Retenciones | RETENCIONES
	# name: str

	# # Impuesto - Nombre 1 | IMPU_ID_IMPU
	# name: str

	# # Impuesto - Nombre 2 | IMPU_ID_IMP2
	# name: str

	# # Concepto 1 | CORE_ID_CORE
	# name: str

	# # Concepto 2 | CORE_ID_CON2
	# name: str

	# # Importe retencion 1 | IMPORTE_RETENCION_1
	# name: str

	# # Importe retencion 2 | IMPUESTO_RETENCION_2
	# name: str

	# # Total retenciones | TOTAL_RETENCIONES
	# name: str

	# # Total a pagar | TOTAL_A_PAGAR
	# name: str

	# # campo TEST | CAMPO_TEST
	# name: str

	# # ID en Uruguay | ID_URUGUAY
	# name: str

	# # Plazo de Pago | PLAZO_DE_PAGO
	# name: str

	# # Plazo de Días de Pago | PLAZO_DE_DIAS_DE_PAG
	# name: str

	# # Prioridad | PRIORIDAD
	# name: str

	# # info contabilidad | INFO_CONTABLE
	# name: str
	fk_yiqi_invoice: int | None = Field(default=None)
