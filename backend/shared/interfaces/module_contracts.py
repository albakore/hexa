"""
Contratos compartidos entre módulos usando Protocol (Structural Subtyping)
Esto permite desacoplar módulos sin necesidad de imports directos
"""

from typing import Protocol, Any, Optional, Sequence
from uuid import UUID


# ============================================================================
# User Module Contracts
# ============================================================================


class UserRepositoryProtocol(Protocol):
	"""Contrato para repositorio de usuarios"""

	async def get_by_id(self, user_id: int) -> Optional[Any]:
		"""Obtiene un usuario por ID"""
		...

	async def get_by_email(self, email: str) -> Optional[Any]:
		"""Obtiene un usuario por email"""
		...

	async def create(self, user_data: Any) -> Any:
		"""Crea un nuevo usuario"""
		...

	async def update(self, user: Any) -> Any:
		"""Actualiza un usuario"""
		...


# ============================================================================
# RBAC Module Contracts
# ============================================================================


class RBACRepositoryProtocol(Protocol):
	"""Contrato para repositorio de RBAC"""

	async def get_permissions_for_user(self, user_id: int) -> Sequence[Any]:
		"""Obtiene permisos de un usuario"""
		...

	async def get_role_by_id(self, role_id: int) -> Optional[Any]:
		"""Obtiene un rol por ID"""
		...

	async def get_roles_for_user(self, user_id: int) -> Sequence[Any]:
		"""Obtiene roles de un usuario"""
		...


# ============================================================================
# Module (AppModule) Contracts
# ============================================================================


class AppModuleRepositoryProtocol(Protocol):
	"""Contrato para repositorio de módulos de aplicación"""

	async def get_by_id(self, module_id: int) -> Optional[Any]:
		"""Obtiene un módulo por ID"""
		...

	async def get_all(self) -> Sequence[Any]:
		"""Obtiene todos los módulos"""
		...

	async def create(self, module_data: Any) -> Any:
		"""Crea un nuevo módulo"""
		...


# ============================================================================
# Yiqi ERP Module Contracts
# ============================================================================


class YiqiServiceProtocol(Protocol):
	"""Contrato para servicio de Yiqi ERP"""

	async def get_currency_by_code(self, code: str, company_id: int) -> dict:
		"""Obtiene moneda por código"""
		...

	async def create_invoice(self, command: Any, company_id: int) -> dict:
		"""Crea una factura en Yiqi ERP"""
		...

	async def upload_file(self, command: Any, company_id: int) -> dict:
		"""Sube un archivo a Yiqi ERP"""
		...


# ============================================================================
# File Storage Module Contracts
# ============================================================================


class FileStorageServiceProtocol(Protocol):
	"""Contrato para servicio de almacenamiento de archivos"""

	async def upload_file(self, file_data: Any) -> Any:
		"""Sube un archivo"""
		...

	async def download_file(self, file_id: UUID) -> Any:
		"""Descarga un archivo"""
		...

	async def get_metadata(self, file_id: UUID) -> Any:
		"""Obtiene metadata de un archivo"""
		...

	async def delete_file(self, file_id: UUID) -> bool:
		"""Elimina un archivo"""
		...


# ============================================================================
# Finance Module Contracts
# ============================================================================


class CurrencyServiceProtocol(Protocol):
	"""Contrato para servicio de monedas"""

	async def get_by_code(self, code: str) -> Optional[Any]:
		"""Obtiene moneda por código"""
		...

	async def get_all(self) -> Sequence[Any]:
		"""Obtiene todas las monedas"""
		...

	async def create(self, currency_data: Any) -> Any:
		"""Crea una nueva moneda"""
		...
