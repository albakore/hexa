"""
Protocolo para servicios del módulo App.

Permite type checking y autocompletado sin crear dependencias directas
entre otros módulos.
"""

from typing import Any, List, Optional, Protocol, Self


class AppModuleServiceProtocol(Protocol):
	"""API pública del módulo AppModule para gestión de módulos de aplicación"""

	def __call__(self) -> Self: ...
	async def get_all_modules(self) -> List[Any]:
		"""Obtiene todos los módulos"""
		...

	async def get_module_by_id(self, id: int) -> Optional[Any]:
		"""Obtiene un módulo por ID"""
		...

	async def create_module(self, command: Any) -> Any:
		"""Crea un nuevo módulo"""
		...

	async def save(self, module: Any) -> Optional[Any]:
		"""Guarda un módulo"""
		...
