from datetime import date
from typing import Optional
from fastapi import File, UploadFile
from pydantic import BaseModel, Field, field_serializer, field_validator


class YiqiInvoice(BaseModel):
	Provider: int = Field(serialization_alias="2880")
	Numero: str = Field(serialization_alias="2879")
	# Sucursal : Optional[int] 										= Field(serialization_alias='5406')
	Concepto: str = Field(serialization_alias="2888")
	# Comprobante : Optional[UploadFile] 							= Field(serialization_alias='2891')
	AWB: Optional[str] = Field(serialization_alias="7102")
	# Detalle : Optional[UploadFile] 								= Field(serialization_alias='5494')
	Servicio: Optional[int] = Field(serialization_alias="6196")
	# Link : Optional[str] 											= Field(serialization_alias='7015')
	# Retenciones_aplicadas : Optional[bool] 						= Field(serialization_alias='7050')
	# Marca_TC : Optional[bool] 									= Field(serialization_alias='6557')
	# Sector : Optional[int] 										= Field(serialization_alias='6558')
	# Banco_Titular : Optional[int] 								= Field(serialization_alias='6564')
	Fecha_emision: date = Field(serialization_alias="2881")
	Fecha_recepcion: date = Field(serialization_alias="5112")
	Mes_servicio: date = Field(serialization_alias="5082")
	Precio_unitario: int | float = Field(serialization_alias="6405")
	# Neto_de_controlador : Optional[int] 							= Field(serialization_alias='6475')
	Moneda_original: Optional[int] = Field(serialization_alias="5074")
	# TC_FACO : Optional[str] 										= Field(serialization_alias='7105')
	# Marca_de_gastos : Optional[bool] 								= Field(serialization_alias='6402')
	# Motivo_de_envio_a_modificaciones_pedidas : Optional[int]		= Field(serialization_alias='6466')
	# Estado_reclamo : Optional[int] 								= Field(serialization_alias='7101')
	# Responsable_ADM : Optional[int] 								= Field(serialization_alias='6231')
	# Responsable_Control_volumen : Optional[int] 					= Field(serialization_alias='6230')
	# Responsable_Control_Tarifa : Optional[int] 					= Field(serialization_alias='6506')
	# Responsable_Cuenta : Optional[int] 							= Field(serialization_alias='6506')
	Kg: Optional[float] = Field(serialization_alias="6599")
	Items: Optional[int] = Field(serialization_alias="6600")
	# Fecha_de_detalles_solicitados : Optional[date] 				= Field(serialization_alias='6906')
	# Impuesto_Nombre_1 : Optional[int] 							= Field(serialization_alias='6951')
	# Impuesto_Nombre_2 : Optional[int] 							= Field(serialization_alias='6954')
	# Contepto_1 : Optional[int]									= Field(serialization_alias='6952')
	# Contepto_2 : Optional[int]									= Field(serialization_alias='6955')
	# Campo_TEST : Optional[str] 									= Field(serialization_alias='7060')
	# ID_en_Uruguay : Optional[str] 								= Field(serialization_alias='7092')
	creado_en_portal: Optional[bool] = Field(serialization_alias="7677")

	model_config = {"extra": "forbid"}

	@field_validator("Fecha_emision", "Fecha_recepcion", "Mes_servicio", mode="after")
	def parse_dob(cls, v):
		return date.strftime(v, "%d/%m/%Y")


class YiqiInvoiceAttach(BaseModel):
	Comprobante: Optional[UploadFile] = File(serialization_alias="2891")
	Detalle: Optional[UploadFile] = File(serialization_alias="5494")

	model_config = {"extra": "forbid"}

	# @field_validator("Comprobante","Detalle", mode="after")
	# def validate_file(cls, value : UploadFile):
	# 	if value:
	# 		return value.filename

	@field_serializer("Comprobante", "Detalle", when_used="always")
	def serialized_file(self, value: UploadFile):
		if value:
			return value.filename


class CreateYiqiInvoiceCommand(YiqiInvoice, YiqiInvoiceAttach): ...


class UploadFileCommand(UploadFile): ...
