"""
Protocolo para servicios del módulo Yiqi ERP.

Permite type checking y autocompletado sin crear dependencias directas
entre otros módulos.
"""

from typing import Any, Protocol, Self, List


class YiqiServiceProtocol(Protocol):
	"""
	API pública del módulo Yiqi ERP.

	Expone operaciones para integración con el ERP externo Yiqi.
	"""

	def __call__(self) -> Self: ...
	async def create_invoice(self, command: Any, id_schema: int) -> dict:
		"""
		Crea una factura en el ERP Yiqi.

		Args:
			command: CreateYiqiInvoiceCommand
			id_schema: ID del schema/empresa

		Used by:
		"""
		...

	async def get_provider_by_id(self, id_provider: int, id_schema: int) -> dict:
		"""Obtiene proveedor del ERP por ID"""
		...

	async def get_services_list(self, id_schema: int) -> List[dict]:
		"""Obtiene lista de servicios del ERP"""
		...

	async def get_currency_list(self, id_schema: int) -> List[dict]:
		"""Obtiene lista de monedas del ERP"""
		...

	async def get_currency_by_code(self, code: str, id_schema: int) -> dict:
		"""
		Obtiene moneda del ERP por código.

		Used by:
		"""
		...

	async def get_country_list(self, id_schema: int = 316) -> List[dict]:
		"""Obtiene lista de países del ERP"""
		...

	async def get_country_by_name(self, name: str, id_schema: int = 316) -> dict:
		"""
		Obtiene país del ERP por nombre.

		Used by:
		"""
		...

	async def get_providers_list(self, id_schema: int) -> List[dict]:
		"""Obtiene lista de proveedores del ERP"""
		...

	async def upload_file(self, command: Any, id_schema: int = 316) -> dict:
		"""
		Sube un archivo al ERP.

		Args:
			command: UploadFileCommand
			id_schema: ID del schema/empresa

		Used by:
		"""
		...


class InvoiceIntegrationServiceProtocol(Protocol):
	"""
	API pública del módulo Yiqi ERP para integración de facturas.

	Orquesta la creación de facturas en YiqiERP desde PurchaseInvoice.
	"""

	def __call__(self) -> Self: ...
	async def create_invoice_from_purchase_invoice(
		self, purchase_invoice_id: int, company_id: int = 316
	) -> dict:
		"""
		Crea una factura en YiqiERP desde una PurchaseInvoice.

		Este método orquesta:
		- Obtención de la PurchaseInvoice
		- Descarga de archivos adjuntos
		- Upload de archivos al ERP
		- Creación de factura en el ERP
		- Actualización de la PurchaseInvoice con el ID de YiqiERP

		Args:
			purchase_invoice_id: ID de la factura de compra
			company_id: ID de la empresa en YiqiERP (default: 316)

		Returns:
			dict: Respuesta del ERP con la factura creada

		Used by: yiqi_erp_tasks (create_invoice_from_purchase_invoice)
		"""
		...


# ============================================================================
# CELERY TASKS PROTOCOLS
# ============================================================================


class YiqiERPTasksProtocol(Protocol):
	"""
	API pública de tasks de Celery del módulo YiqiERP.

	Estas tasks se ejecutan de forma asíncrona a través de Celery.
	Cada task tiene el método .delay() para ejecución asíncrona.
	"""

	def __call__(self) -> Self: ...
	def create_invoice_from_purchase_invoice(
		self, purchase_invoice_id: int, company_id: int = 316
	) -> dict:
		"""
		Task para crear factura en YiqiERP desde una PurchaseInvoice.

		Esta función se ejecutará de forma asíncrona a través de Celery.
		Nombre registrado: "yiqi_erp.create_invoice_from_purchase_invoice"

		Args:
			purchase_invoice_id: ID de la factura de compra
			company_id: ID de la empresa en YiqiERP (default: 316)

		Usage:
			tasks = service_locator.get_service("yiqi_erp_tasks")
			tasks["create_invoice_from_purchase_invoice"].delay(123)

		Returns:
			dict: Respuesta del ERP con la factura creada

		Used by: draft_purchase_invoice_service (finalize_and_emit_invoice)
		"""
		...
