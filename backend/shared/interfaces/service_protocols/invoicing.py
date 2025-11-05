"""
Protocolo para servicios del módulo Invoicing.

Permite type checking y autocompletado sin crear dependencias directas
entre otros módulos.
"""

from typing import Any, Optional, Protocol, Self, List


class PurchaseInvoiceServiceProtocol(Protocol):
	"""API pública del módulo Invoicing para gestión de facturas de compra"""

	def __call__(self) -> Self: ...
	async def get_list(self, limit: int = 20, page: int = 0) -> List[Any]:
		"""Obtiene lista paginada de facturas de compra"""
		...

	async def get_list_of_provider(
		self, id_provider: int, limit: int, page: int
	) -> List[Any]:
		"""Obtiene lista de facturas de un proveedor"""
		...

	async def get_one_by_id(self, id_purchase_invoice: int) -> Optional[Any]:
		"""
		Obtiene factura de compra por ID.

		Used by:
		"""
		...

	async def create(self, command: Any) -> Any:
		"""
		Crea una nueva factura de compra.

		Used by: invoice_orchestrator_service
		"""
		...

	async def save(self, purchase_invoice: Any) -> Any:
		"""
		Guarda una factura de compra.

		Used by: invoice_orchestrator_service,
		"""
		...

	async def save_and_emit(self, purchase_invoice: Any) -> Any:
		"""
		Guarda una factura de compra y lo emite a yiqi.

		Used by: draft_purchase_invoice_service
		"""
		...


class InvoiceOrchestratorServiceProtocol(Protocol):
	"""
	API pública del módulo Invoicing para orquestación de facturas.

	Coordina la creación de facturas desde drafts y envío a sistemas externos.
	"""

	def __call__(self) -> Self: ...
	async def create_invoice_from_draft(self, draft_purchase_invoice_id: int) -> Any:
		"""
		Crea una PurchaseInvoice desde un DraftPurchaseInvoice.

		Este método orquesta:
		- Obtención del draft
		- Creación de PurchaseInvoice
		- Envío de task a YiqiERP
		- Actualización del estado del draft

		Args:
			draft_purchase_invoice_id: ID del borrador de factura

		Returns:
			PurchaseInvoice creada

		Used by: API endpoints, workflows
		"""
		...


# ============================================================================
# CELERY TASKS PROTOCOLS
# ============================================================================


class InvoicingTasksProtocol(Protocol):
	"""
	API pública de tasks de Celery del módulo Invoicing.

	Estas tasks se ejecutan de forma asíncrona a través de Celery.
	Cada task tiene el método .delay() para ejecución asíncrona.
	"""

	def __call__(self) -> Self: ...
	def emit_invoice(self) -> str:
		"""
		Task para emitir factura.

		Esta función se ejecutará de forma asíncrona a través de Celery.
		Nombre registrado: "invoicing.emit_invoice"

		Usage:
			tasks = service_locator.get_service("invoicing_tasks")
			tasks["emit_invoice"].delay()

		Returns:
			str: Mensaje de confirmación
		"""
		...
