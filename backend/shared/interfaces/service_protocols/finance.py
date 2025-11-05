"""
Protocolo para servicios del módulo Finance.

Permite type checking y autocompletado sin crear dependencias directas
entre otros módulos.
"""

from typing import Any, Optional, Protocol, Self, List


class CurrencyServiceProtocol(Protocol):
	"""
	API pública del módulo Finance para gestión de monedas.
	"""

	def __call__(self) -> Self: ...
	async def get_currency_list(self) -> List[Any]:
		"""Obtiene lista de todas las monedas"""
		...

	async def get_currency_by_id(self, id_currency: int) -> Optional[Any]:
		"""Obtiene moneda por ID"""
		...

	async def create_currency(self, command: Any) -> Any:
		"""Crea una entidad Currency (sin guardar)"""
		...

	async def create_currency_and_save(self, command: Any) -> Any:
		"""
		Crea y guarda una nueva moneda.

		Used by: admin, finance operations
		"""
		...

	async def update_currency(self, command: Any) -> Any:
		"""Actualiza una moneda existente"""
		...

	async def save_currency(self, currency: Any) -> Any:
		"""Guarda una moneda"""
		...

	async def delete_currency(self, id_currency: int) -> Any:
		"""Elimina una moneda"""
		...
