"""
Protocolos compartidos para servicios de aplicación.

Estos protocolos definen las APIs públicas de todos los módulos del sistema,
permitiendo type checking y autocompletado sin crear dependencias directas
entre módulos.

Cada Protocol debe mantenerse sincronizado con su servicio correspondiente.
"""

from typing import Protocol, Optional, List, Self, Sequence, Any
from datetime import date
from uuid import UUID


# ============================================================================
# USER MODULE
# ============================================================================


class UserServiceProtocol(Protocol):
	"""
	API pública del módulo User.

	Expone operaciones para gestión de usuarios.
	"""

	def __call__(self) -> Self: ...

	async def get_user_list(self, limit: int, page: int) -> List[Any]:
		"""Obtiene lista de usuarios paginada"""
		...

	async def get_user_by_id(self, user_id: int) -> Optional[Any]:
		"""Obtiene usuario por ID"""
		...

	async def get_user_by_uuid(self, user_uuid: str) -> Optional[Any]:
		"""Obtiene usuario por UUID"""
		...

	async def get_user_by_email_or_nickname(
		self, email: str, nickname: str, with_role: bool = False
	) -> Optional[Any]:
		"""
		Obtiene usuario por email o nickname.

		Args:
			email: Email del usuario
			nickname: Nickname del usuario
			with_role: Si debe incluir información del rol

		Used by: auth (login, register)
		"""
		...

	async def save_user(self, user: Any) -> Any:
		"""
		Guarda un usuario.

		Used by: auth (register)
		"""
		...

	async def set_user_password(self, user: Any, hashed_password: str) -> Any:
		"""
		Establece la contraseña de un usuario.

		Used by: auth (password reset)
		"""
		...

	async def create_user(self, *, command: Any) -> Optional[Any]:
		"""Crea un nuevo usuario"""
		...

	async def asign_role_to_user(self, user_uuid: str, role_id: int) -> Any:
		"""Asigna un rol a un usuario"""
		...

	async def get_all_user_with_roles(
		self, role_id_list: List[int]
	) -> List[Any] | Sequence[Any]:
		"""Obtiene todos los usuarios con roles específicos"""
		...


# ============================================================================
# RBAC MODULE
# ============================================================================


class RoleServiceProtocol(Protocol):
	"""
	API pública del módulo RBAC para gestión de roles.

	Expone operaciones para gestión de roles, permisos y módulos.
	"""

	def __call__(self) -> Self: ...

	async def get_all_roles(self) -> List[Any]:
		"""Obtiene todos los roles"""
		...

	async def get_role_by_id(
		self,
		id_role: int,
		with_permissions: bool = False,
		with_groups: bool = False,
		with_modules: bool = False,
	) -> Optional[Any]:
		"""
		Obtiene un rol por ID.

		Used by: auth (jwt refresh token)
		"""
		...

	async def get_permissions_from_role(self, role: Any) -> List[Any]:
		"""
		Obtiene todos los permisos de un rol.

		Used by: auth (login, jwt refresh)
		"""
		...

	async def get_modules_from_role_entity(self, role: Any) -> List[Any]:
		"""
		Obtiene todos los módulos de un rol.

		Used by: auth (login, jwt refresh)
		"""
		...

	async def get_modules_from_role(self, role: Any) -> List[Any]:
		"""Obtiene módulos de un rol"""
		...

	async def create_role(self, command: Any) -> Any:
		"""Crea un nuevo rol"""
		...

	async def save(self, role: Any) -> Optional[Any]:
		"""Guarda un rol"""
		...

	async def delete(self, id: int) -> None:
		"""Elimina un rol"""
		...

	async def edit_role(self, id_role: int, command: Any) -> Any:
		"""Edita un rol existente"""
		...

	async def append_permissions_to_role(
		self, permissions: List[Any], id_role: int
	) -> Any:
		"""Añade permisos a un rol"""
		...

	async def append_groups_to_role(self, groups: List[Any], id_role: int) -> Any:
		"""Añade grupos de permisos a un rol"""
		...

	async def append_modules_to_role(self, modules: List[Any], id_role: int) -> Any:
		"""Añade módulos a un rol"""
		...

	async def remove_permissions_to_role(
		self, permissions: List[Any], id_role: int
	) -> int:
		"""Remueve permisos de un rol"""
		...

	async def remove_group_permissions_to_role(
		self, groups: List[Any], id_role: int
	) -> int:
		"""Remueve grupos de permisos de un rol"""
		...

	async def remove_modules_to_role(self, modules: List[Any], id_role: int) -> Any:
		"""Remueve módulos de un rol"""
		...

	async def get_all_roles_from_modules(self, id_modules: List[int]) -> List[Any]:
		"""Obtiene roles asociados a módulos específicos"""
		...


class PermissionServiceProtocol(Protocol):
	"""API pública del módulo RBAC para gestión de permisos"""

	def __call__(self) -> Self: ...

	async def get_all_permissions(self) -> List[Any]:
		"""Obtiene todos los permisos"""
		...

	async def get_permission_by_id(self, id: int) -> Optional[Any]:
		"""Obtiene un permiso por ID"""
		...


# ============================================================================
# APP MODULE
# ============================================================================


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


# ============================================================================
# FILE STORAGE MODULE
# ============================================================================


class FileStorageServiceProtocol(Protocol):
	"""
	API pública del módulo FileStorage.

	Expone operaciones para gestión de archivos en S3/storage.
	"""

	def __call__(self) -> Self: ...
	async def save_file(self, command: Any) -> Optional[Any]:
		"""
		Guarda un archivo en el storage.

		Args:
			command: SaveFileCommand con file, filename, size

		Returns:
			FileMetadata del archivo guardado

		Used by: provider (draft invoices)
		"""
		...

	async def download_file(self, file_metadata_uuid: UUID) -> Any:
		"""
		Descarga un archivo del storage.

		Returns:
			FileStorageDTO con (file: bytes, metadata: FileMetadata)

		Used by: provider (finalize invoice)
		"""
		...

	async def get_metadata(self, file_metadata_uuid: UUID) -> Any:
		"""
		Obtiene metadata de un archivo.

		Returns:
			FileMetadata

		Used by: provider (draft invoices)
		"""
		...


# ============================================================================
# FINANCE MODULE
# ============================================================================


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


# ============================================================================
# YIQI ERP MODULE
# ============================================================================


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

		Used by: provider (finalize draft invoice)
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

		Used by: provider (finalize draft invoice)
		"""
		...

	async def upload_file(self, command: Any, id_schema: int) -> dict:
		"""
		Sube un archivo al ERP.

		Args:
			command: UploadFileCommand
			id_schema: ID del schema/empresa

		Used by: provider (finalize draft invoice - upload attachments)
		"""
		...


# ============================================================================
# PROVIDER MODULE
# ============================================================================


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
		"""Obtiene borrador de factura por ID"""
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
		"""Guarda un borrador de factura"""
		...

	async def delete_draft_purchase_invoice(
		self, id_draft_purchase_invoice: int
	) -> Any:
		"""Elimina un borrador de factura"""
		...

	async def finalize_and_emit_invoice(self, id_draft_purchase_invoice: int) -> dict:
		"""
		Finaliza un borrador y lo emite al ERP.

		Este método coordina:
		- Obtención de archivos del storage
		- Upload de archivos al ERP
		- Creación de factura en el ERP
		- Actualización del estado del borrador
		"""
		...


class PurchaseInvoiceServiceTypeServiceProtocol(Protocol):
	"""API pública para gestión de tipos de servicio en facturas de compra"""

	def __call__(self) -> Self: ...
	async def get_all_service_types(self, limit: int, page: int) -> List[Any]:
		"""Obtiene lista de tipos de servicio"""
		...

	async def get_service_type_by_id(self, id_service_type: int) -> Optional[Any]:
		"""Obtiene tipo de servicio por ID"""
		...


# ============================================================================
# INVOICING MODULE
# ============================================================================


class PurchaseInvoiceServiceProtocol(Protocol):
	"""API pública del módulo Invoicing para gestión de facturas de compra"""

	def __call__(self) -> Self: ...
	async def get_list(self, limit: int = 20, page: int = 0) -> List[Any]:
		"""Obtiene lista paginada de facturas de compra"""
		...

	async def get_by_id(self, id_purchase_invoice: int) -> Optional[Any]:
		"""Obtiene factura de compra por ID"""
		...

	async def create(self, command: Any) -> Any:
		"""Crea una nueva factura de compra"""
		...

	async def save(self, purchase_invoice: Any) -> Any:
		"""Guarda una factura de compra"""
		...

	async def delete(self, id_purchase_invoice: int) -> Any:
		"""Elimina una factura de compra"""
		...


# ============================================================================
# AUTH MODULE
# ============================================================================


class AuthServiceProtocol(Protocol):
	"""API pública del módulo Auth para autenticación"""

	def __call__(self) -> Self: ...
	async def login(self, email_or_nickname: str, password: str) -> Any:
		"""
		Realiza login de usuario.

		Returns:
			LoginResponseDTO o AuthPasswordResetResponseDTO
		"""
		...

	async def register(self, registration_data: Any) -> Any:
		"""Registra un nuevo usuario"""
		...

	async def password_reset(
		self, user_uuid: str, initial_password: str, new_password: str
	) -> bool:
		"""Resetea la contraseña de un usuario"""
		...


class JwtServiceProtocol(Protocol):
	"""API pública del módulo Auth para gestión de JWT tokens"""

	def __call__(self) -> Self: ...
	async def verify_token(self, token: str) -> dict:
		"""Verifica y decodifica un JWT token"""
		...

	async def create_refresh_token(self, refresh_token: str) -> Any:
		"""
		Crea nuevo access token desde refresh token.

		Returns:
			RefreshTokenResponseDTO
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


class YiqiERPTasksProtocol(Protocol):
	"""
	API pública de tasks de Celery del módulo YiqiERP.

	Estas tasks se ejecutan de forma asíncrona a través de Celery.
	Cada task tiene el método .delay() para ejecución asíncrona.
	"""

	def __call__(self) -> Self: ...
	def emit_invoice(self, data: Any) -> str:
		"""
		Task para emitir factura al ERP externo Yiqi.

		Esta función se ejecutará de forma asíncrona a través de Celery.
		Nombre registrado: "yiqi_erp.emit_invoice"

		Args:
			data: Datos de la factura a emitir (dict serializable)

		Usage:
			tasks = service_locator.get_service("yiqi_erp_tasks")
			tasks["emit_invoice"].delay({"invoice_id": 123})

		Returns:
			str: Mensaje de confirmación

		Used by: invoicing (purchase_invoice endpoint)
		"""
		...


class NotificationsTasksProtocol(Protocol):
	"""
	API pública de tasks de Celery del módulo Notifications.

	Estas tasks se ejecutan de forma asíncrona a través de Celery.
	Cada task tiene el método .delay() para ejecución asíncrona.
	"""

	def __call__(self) -> Self: ...
	def send_notification(self) -> str:
		"""
		Task para enviar notificación.

		Esta función se ejecutará de forma asíncrona a través de Celery.
		Nombre registrado: "notifications.send_notification"

		Usage:
			tasks = service_locator.get_service("notifications_tasks")
			tasks["send_notification"].delay()

		Returns:
			str: Mensaje de confirmación
		"""
		...
