"""
Protocolo para servicios del módulo Provider.

Permite type checking y autocompletado sin crear dependencias directas
entre otros módulos.
"""

from typing import Any, Optional, Protocol, Self, List, Sequence


class ProviderServiceProtocol(Protocol):
	"""API pública del módulo Provider para gestión de proveedores"""

	def __call__(self) -> Self: ...
	async def get_all_providers(self, limit: int, page: int) -> List[Any]:
		"""Obtiene lista paginada de proveedores"""
		...

	async def get_provider_by_id(self, id_provider: int) -> Optional[Any]:
		"""Obtiene proveedor por ID"""
		...

	async def create_provider(self, command: Any) -> Any:
		"""Crea un nuevo proveedor"""
		...

	async def save_provider(self, provider: Any) -> Any:
		"""Guarda un proveedor"""
		...


class DraftPurchaseInvoiceServiceProtocol(Protocol):
	"""API pública del módulo Provider para gestión de borradores de facturas"""

	def __call__(self) -> Self: ...
	async def get_all_draft_purchase_invoices(
		self, id_provider: int, limit: int = 20, page: int = 0
	) -> List[Any] | Sequence[Any]:
		"""Obtiene borradores de facturas de un proveedor"""
		...

	async def get_draft_purchase_invoice_by_id(
		self, id_draft_purchase_invoice: int
	) -> Any:
		"""
		Obtiene borrador de factura por ID.

		Used by: invoice_orchestrator_service
		"""
		...

	async def get_draft_purchase_invoice_with_filemetadata(
		self, draft_purchase_invoice: Any
	) -> Any:
		"""Obtiene borrador con metadata de archivos adjuntos"""
		...

	async def create_draft_purchase_invoice(self, command: Any) -> Any:
		"""Crea un nuevo borrador de factura"""
		...

	async def save_draft_purchase_invoice(self, draft_purchase_invoice: Any) -> Any:
		"""
		Guarda un borrador de factura.

		Used by: invoice_orchestrator_service
		"""
		...

	async def delete_draft_purchase_invoice(
		self, id_draft_purchase_invoice: int
	) -> Any:
		"""Elimina un borrador de factura"""
		...

	async def finalize_draft(self, id_draft_purchase_invoice: int) -> Any:
		"""
		Finaliza un draft marcándolo como listo para ser procesado.
		Solo valida y cambia el estado, NO crea facturas.
		"""
		...


class PurchaseInvoiceServiceTypeServiceProtocol(Protocol):
	"""API pública para gestión de tipos de servicio en facturas de compra"""

	def __call__(self) -> Self: ...
	async def get_all_service_types(self, limit: int, page: int) -> List[Any]:
		"""Obtiene lista de tipos de servicio"""
		...

	async def get_services_by_id(self, id_service_type: int) -> Optional[Any]:
		"""Obtiene tipo de servicio por ID"""
		...


class AirWaybillServiceProtocol(Protocol):
	"""API pública del módulo Provider para gestión de guías aéreas"""

	def __call__(self) -> Self: ...
	async def get_air_waybill_by_id(self, id_air_waybill: int) -> Optional[Any]:
		"""Obtiene guía aérea por ID"""
		...

	async def get_air_waybills_by_draft_invoice_id(
		self, id_draft_invoice: int
	) -> List[Any] | Sequence[Any]:
		"""Obtiene guías aéreas asociadas a una factura Draft"""
		...

	async def get_air_waybills_by_purchase_invoice_id(
		self, id_purchase_invoice: int
	) -> List[Any] | Sequence[Any]:
		"""Obtiene guías aéreas asociadas a una factura"""
		...

	async def create_air_waybill(self, command: Any) -> Any:
		"""Crea una nueva guía aérea"""
		...

	async def save_air_waybill(self, air_waybill: Any) -> Any:
		"""Guarda una guía aérea"""
		...

	async def update_air_waybill(self, command: Any) -> Any:
		"""Actualiza una guía aérea existente"""
		...

	async def delete_air_waybill(self, air_waybill: Any) -> Any:
		"""Elimina una guía aérea"""
		...
