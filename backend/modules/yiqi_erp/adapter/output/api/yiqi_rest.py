import json
import time
import urllib.parse
from dataclasses import dataclass
from fastapi import UploadFile

from modules.yiqi_erp.adapter.output.api.http_client import YiqiHttpClient
from modules.yiqi_erp.domain.command import (
	CreateYiqiAirWaybillCommand,
	CreateYiqiInvoiceCommand,
	YiqiAirWaybill,
	YiqiInvoice,
	YiqiInvoiceAttach,
)
from modules.yiqi_erp.domain.repository.yiqi import YiqiRepository
from modules.yiqi_erp.adapter.output.api.exception import RequestException
from core.config.settings import env
from starlette.datastructures import Headers


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
		entity_name = "SERVICIOS"
		last_update = "01011900"
		aditional_filters = [
			# {
			# 	"columnName": "PORT_ACTIVO_EN_PORTAL",
			# 	"TipoDato": 2,
			# 	"operator": 3,
			# 	"operating": "1",
			# }
		]

		attributes = [
			# "SERV_ID",
			"SERV_SERVICIO",
			"SERV_MARCA_DE_GASTOS",
			"SERV_ACTIVO_PRO",
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

	async def get_country_list(self, id_schema: int = 316):
		url = "/api/InstancesAPI/GetEntityUpdates2"
		entity_name = "PAIS"
		last_update = "01011900"
		aditional_filters = []
		attributes = ["PAIS_PAIS", "PAIS_CODIGO"]
		params = {
			"schemaId": id_schema,
			"entityName": entity_name,
			"lastUpdate": last_update,
			"additionalFilters": aditional_filters.__repr__(),
			"attributes": ",".join(attributes),
		}
		response = await self.client.get(url, params)
		return response

	async def get_country_by_name(
		self, country_name: str, id_schema: int = 316
	) -> dict | None:
		url = "/api/InstancesAPI/GetEntityUpdates2"
		entity_name = "PAIS"
		last_update = "01011900"

		aditional_filters = [
			{
				"columnName": "PAIS_PAIS",
				"TipoDato": 2,
				"operator": 1,
				"operating": str(country_name),
			}
		]

		attributes = ["PAIS_PAIS", "PAIS_CODIGO"]
		params = {
			"schemaId": id_schema,
			"entityName": entity_name,
			"lastUpdate": last_update,
			"additionalFilters": aditional_filters.__repr__(),
			"attributes": ",".join(attributes),
		}
		response = await self.client.get(url, params)
		# Consulto si la respuesta esta ok
		if response.is_success:
			# Paso la respuesta diccionario
			data_list = response.json()
			# Como se que esto me devuelve una lista, trato de respetar
			# y devolver una sola instancia
			if len(data_list) > 0:
				instance = data_list[0]
				return instance
			# En caso de que no haya nada, va a devolver a una lista vacia
			# asi que devuelvo none porque, volviendo, necesito respetar el metodo heredado
			return None
		# Y si hubo un error o no es 200 o is_success, que devuelva un error
		raise RequestException(code=response.status_code, message=response.text)

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
	) -> dict:
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
		raise Exception("Error creating invoice in YiqiERP", response.text)

	async def create_air_waybill(
		self,
		command: CreateYiqiAirWaybillCommand,
		id_schema: int = 316,
	) -> dict:
		url = "/api/InstancesAPI/SaveInstancePOST2"
		body = YiqiAirWaybill.model_validate(command).model_dump(by_alias=True)

		payload = {
			"schemaId": id_schema,
			"entityName": "GUIAS_AEREAS",
			"jsonNewFiles": "{}",
			"jsonRemovedFiles": "[]",
			"json": json.dumps(body, default=str),
		}

		response = await self.client.post(url, json=payload)
		if response.is_error:
			raise Exception("Error creating air waybill in YiqiERP", response.text)
		return response.json()

	async def create_multiple_air_waybills(
		self, file: UploadFile, id_schema: int = 316
	) -> dict:
		url = "/api/instancesApi/uploadExcel"
		params = {"entityId": 1044}
		data = {
			"schemaId": id_schema,
		}
		headers = {
			"Referer": f"https://me.yiqi.com.ar/view/GUIAS_AEREAS?schemaId={id_schema}"
		}
		files = {"fileUpload": (file.filename, file.file, file.content_type)}
		upload_file = await self.client.post(
			url,
			params=params,
			data=data,
			files=files,
			headers=headers,
		)
		if upload_file.is_error:
			raise Exception(
				"Error creating multiple air waybills in YiqiERP", upload_file.text
			)

		file_path = upload_file.text
		print(f"DEBUG: File path from uploadExcel: {file_path}")
		url = "/api/instancesApi/ImportExcel"
		import_file = await self.client.get(
			url,
			params={
				"schemaId": id_schema,
				"entityId": 1044,
				"updateOnDuplicatePK": "true",
				"parentInstanceId": "null",
				"filePath": file_path,  # Pass the file path from uploadExcel
			},
			headers=headers,
		)
		if import_file.is_error:
			raise Exception(
				"Error importing multiple air waybills in YiqiERP", import_file.text
			)

		while True:
			time.sleep(1)
			process = await self.client.get(
				"/api/instancesApi/GetProgress",
				params={
					"schemaId": id_schema,
					"entityId": 1044,
					"processKey": "EXCIMP",
				},
				headers=headers,
			)
			if process.is_error:
				raise Exception(
					"Error getting import progress of multiple air waybills in YiqiERP",
					process.text,
				)
			process = process.text
			print(f"debug: ${process}")
			if "100|OK" in process:
				break
			if "|ERROR|" in process:
				raise Exception(
					"Error during import of multiple air waybills in YiqiERP", process
				)
				break
		return {"status": "ok"}

	async def get_air_waybills_template_file(self, id_schema: int = 316):
		url = "/api/instancesApi/GenerateExcelTemplate"
		params = {"schemaId": id_schema, "entityId": 1044}
		template_response = await self.client.get(
			url,
			params=params,
			headers={
				"Referer": f"https://me.yiqi.com.ar/view/GUIAS_AEREAS?schemaId={id_schema}"
			},
		)
		if template_response.is_error:
			raise Exception(
				"Error getting air waybills template in YiqiERP", template_response.text
			)
		file_path = template_response.text
		url = env.YIQI_BASE_URL + file_path.replace('"', "")
		print("DEBUG url:", url)
		response = await self.client.get(
			url,
			headers={
				"Referer": f"https://me.yiqi.com.ar/view/GUIAS_AEREAS?schemaId={id_schema}"
			},
		)
		print("DEBUG response:", response.text)
		if response.is_error:
			raise Exception(
				"Error downloading air waybills template in YiqiERP", response.text
			)
		headers = Headers(
			headers={
				"Content-Type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
			}
		)
		file = UploadFile(
			filename="air_waybills_template.xlsx",
			file=response.content,
			headers=headers,
		)
		print("DEBUG file:", file)
		return file

	async def get_air_waybills_by_invoice_id(
		self, id_invoice: int, id_schema: int = 316
	):
		url = "/api/InstancesAPI/GetEntityUpdates2"
		entity_name = "GUIAS_AEREAS"
		last_update = "01011900"
		aditional_filters = [
			{
				"columnName": "FACO_ID_FACO",
				"TipoDato": 2,
				"operator": 1,
				"operating": str(id_invoice),
			}
		]
		attributes = [
			"CLIE_ID_CLIE",
			"FACO_ID_FACO",
			"GUAE_GUIA_AEREA",
			# "GUAE_CN38",
			"PAIS_ID_PAI1",
			"PAIS_ID_PAIS",
			"GUAE_KG",
			# "GUAE_BAGS",
		]
		params = {
			"schemaId": id_schema,
			"entityName": entity_name,
			"lastUpdate": last_update,
			"additionalFilters": aditional_filters.__repr__(),
			"attributes": ",".join(attributes),
		}
		response = await self.client.get(url, params)
		if response.is_success:
			data_list = response.json()
			if len(data_list) > 0:
				return data_list
			return None
		raise RequestException(code=response.status_code, message=response.text)

	async def upload_file(self, file: UploadFile, id_schema: int = 316):
		url = "/api/InstancesAPI/SaveFile"
		data = {
			"SchemaId": id_schema,
		}
		files = {"FileName": (file.filename, file.file, file.content_type)}
		response = await self.client.post(url, data=data, files=files)
		return response

	async def get_providers_list(self, id_schema: int = 316):
		url = "/api/InstancesAPI/GetEntityUpdates2"
		entity_name = "CLIENTE"
		last_update = "01011900"
		aditional_filters = [
			{
				"columnName": "CLIE_ACTIVO_P",
				"TipoDato": 2,
				"operator": 1,
				"operating": "S",
			}
		]
		attributes = [
			"CLIE_NOMBRE",
			"CLIE_RAZON_SOCIAL",
			"CLIE_CUIT",
			"CLIE_MONEDA",
			"CLIE_REGION",
			"CLIE_IDIOMA",
			"CLIE_ACTIVO_P",
			"CLIE_ACTIVO",
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
