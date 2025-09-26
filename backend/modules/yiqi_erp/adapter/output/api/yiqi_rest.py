from dataclasses import dataclass
import urllib.parse

from fastapi import UploadFile

# from backend.modules.yiqi_erp.domain.entity import FacturaDeCompra
from modules.yiqi_erp.adapter.output.api.http_client import YiqiHttpClient
from modules.yiqi_erp.domain.command import (
	CreateYiqiInvoiceCommand,
	YiqiInvoice,
	YiqiInvoiceAttach,
)
from modules.yiqi_erp.domain.repository.yiqi import YiqiRepository


@dataclass
class YiqiApiRepository(YiqiRepository):
	client: YiqiHttpClient

	async def get_provider_by_id(self, id_provider: int, id_schema: int = 316):
		url = "/api/public/CLIENTE"
		params = {"id": id_provider, "schemaId": id_schema}
		response = await self.client.get(url, params)
		return response

	async def get_contact_by_id(self, id_contact: int, id_schema: int = 316):
		url = "/api/public/CONTACTO"
		params = {"id": id_contact, "schemaId": id_schema}
		response = await self.client.get(url, params)
		return response

	async def get_services_list(self, id_schema: int = 316):
		url = "/api/InstancesAPI/GetEntityUpdates2"
		entity_name = "PORTAL_SERVICIO"
		last_update = "01011900"
		aditional_filters = [
			{
				"columnName": "PORT_ACTIVO_EN_PORTAL",
				"TipoDato": 2,
				"operator": 3,
				"operating": "1",
			}
		]

		attributes = [
			# "SERV_ID",
			"PORT_NOMBRE_DEL_SERVICIO",
			"PORT_DESCRIPCION_INGLES",
			"PORT_ACTIVO_EN_PORTAL",
			"PORT_CAMPO_AWB",
			"PORT_CAMPO_ITEMS",
			"PORT_CAMPO_KG",
		]

		params = {
			"schemaId": id_schema,
			"entityName": entity_name,
			"lastUpdate": last_update,
			"additionalFilters": aditional_filters.__repr__(),
			"attributes": ",".join(attributes),
		}
		response = await self.client.get(url, params)
		return response

	async def get_services_list_by_provider_id(self, id_provider: int):
		raise NotImplementedError

	async def get_currency_list(self, id_schema: int = 316):
		url = "/api/InstancesAPI/GetEntityUpdates2"
		entity_name = "MONEDA"
		last_update = "01011900"
		aditional_filters = []
		attributes = ["MONE_NOMBRE", "PAIS_PAIS"]
		params = {
			"schemaId": id_schema,
			"entityName": entity_name,
			"lastUpdate": last_update,
			"additionalFilters": aditional_filters.__repr__(),
			"attributes": ",".join(attributes),
		}
		response = await self.client.get(url, params)
		return response

	async def get_currency_by_code(self, code: str, id_schema: int = 316):
		url = "/api/InstancesAPI/GetEntityUpdates2"
		entity_name = "MONEDA"
		last_update = "01011900"

		aditional_filters = [
			{
				"columnName": "MONE_NOMBRE",
				"TipoDato": 2,
				"operator": 1,
				"operating": str(code),
			}
		]

		attributes = [
			"MONE_NOMBRE",
			"PAIS_PAIS",
		]
		params = {
			"schemaId": id_schema,
			"entityName": entity_name,
			"lastUpdate": last_update,
			"additionalFilters": aditional_filters.__repr__(),
			"attributes": ",".join(attributes),
		}
		response = await self.client.get(url, params)
		return response

	async def get_invoices_list_of_provider(
		self, id_provider: int, id_schema: int = 316
	):
		url = "/api/InstancesAPI/GetEntityUpdates2"
		entity_name = "FACTURA_COMPRA"
		last_update = "01011900"

		"""Tipos de datos
		1: format string
		2: string
		3: datetime
		4: boolean (1 = true, 0 = false)
		"""

		aditional_filters = [
			{
				"columnName": "CLIE_ID_PROV",
				"TipoDato": 2,
				"operator": 1,
				"operating": str(id_provider),
			}
		]

		# attributes = FacturaDeCompra.attibutes()

		attributes = [
			"FACO_ID_FACTURA",
			"CLIE_ID_PROV",
			"FACO_NUMERO",
			# "FACO_ESTADO_DE_EMPRESA",
			"DESC_ESTADO",
			"FACO_CONCEPTO",
			"FACO_ARHC_ID_2736",
			"FACO_DETALLE_ADJ",
			"SERV_ID_SERV",
			# "FACO_PAIS",
			# "FACO_LINK",
			"FACO_AWB",
			"FACO_KG",
			"FACO_ITEMS",
			"FACO_FECHA_EMISION",
			"FACO_FECHA_DE_RECEPCION",
			"FACO_MES_DE_SERVICIO",
			# "FACO_FECHA_PERIODO_DESDE",
			# "FACO_FECHA_PERIODO_HASTA",
			"FACO_NETO",
			# "FACO_IVA",
			# "FACO_TOTAL_1V",
			# "FACO_IVA_USD",
			# "FACO_TOTAL_NOTA_DE_CREDIT",
			# "FACO_USD_NC",
			# "FACO_PENDIENTE_PAGO",
			"MONE_ID_MONE",
			"FACO_SALDO",
			# "FACO_SALDO_USD",
			# "FACO_CANCELACION",
			# "FACO_CANCELACION_USD",
			# "FACO_MOTIVO_DE_ANULACION",
			# "FACO_FECHA_DE_PAGO",
			# "FACO_TOTAL_RETENCIONES",
			# "FACO_TOTAL_A_PAGAR",
			"AUDI_FECHA_ALTA",
		]

		params = {
			"schemaId": id_schema,
			"entityName": entity_name,
			"lastUpdate": last_update,
			"additionalFilters": aditional_filters.__repr__(),
			"attributes": ",".join(attributes),
		}

		response = await self.client.get(url, params)
		return response

	async def create_invoice(
		self,
		command: CreateYiqiInvoiceCommand,
		id_schema: int = 316,
		id_parent: bool | None = None,
		id_child: bool | None = None,
		id_entity: int = 660,
	):
		url = "/api/InstancesAPI/Save"

		form = YiqiInvoice.model_validate(command).model_dump(
			exclude={"Comprobante", "Detalle"}, by_alias=True
		)
		attachs = YiqiInvoiceAttach.model_validate(command).model_dump(
			include={"Comprobante", "Detalle"},
			by_alias=True,
			exclude_none=True,
		)

		# for key, value in attachs.copy().items():
		# 	if not value:
		# 		del attachs[key]
		# r.print(attachs)
		json = {
			"schemaId": id_schema,
			"form": urllib.parse.urlencode(form),
			"uploads": urllib.parse.urlencode(attachs),
			"parentId": id_parent,
			"childId": id_child,
			"entityId": str(id_entity),
		}

		response = await self.client.post(url, json=json)
		if response.is_success:
			return response.json()
		return response.text

	async def upload_file(self, file: UploadFile, id_schema: int = 316):
		url = "/api/InstancesAPI/SaveFile"
		data = {
			"SchemaId": id_schema,
		}
		files = {"FileName": (file.filename, file.file, file.content_type)}
		response = await self.client.post(url, data=data, files=files)
		return response
