"""
Sistema de validación de permisos usando Security de FastAPI.

Este módulo proporciona una función que se puede usar con Security()
para validar permisos en endpoints de FastAPI.
"""

from typing import List
from fastapi import Request, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.authentication import UnauthenticatedUser
from starlette import status


# Esquema de seguridad para Swagger
security_scheme = HTTPBearer()


def require_permissions(*permissions: str):
	"""
	Factory function que crea una dependency de seguridad para validar permisos.

	Esta función se usa con Security() de FastAPI para validar que el usuario
	autenticado tenga los permisos requeridos.

	Args:
		*permissions: Tokens de permisos requeridos (ej: "users:read", "invoices:write")

	Returns:
		Una función async que FastAPI ejecutará como dependency

	Ejemplo:
		from fastapi import Security

		@router.get("/users")
		async def get_users(
			_: None = Security(require_permissions("users:read"))
		):
			return {"users": []}

		@router.post("/invoices")
		async def create_invoice(
			_: None = Security(require_permissions("invoices:create", "invoices:write"))
		):
			return {"created": True}
	"""

	async def permission_checker(
		request: Request,
		credentials: HTTPAuthorizationCredentials = Security(security_scheme),
	) -> None:
		"""
		Valida que el usuario autenticado tenga todos los permisos requeridos.

		Args:
			request: Request de FastAPI (contiene request.user del AuthenticationMiddleware)
			credentials: Credenciales del header Authorization (automático por HTTPBearer)

		Raises:
			HTTPException: 401 si no está autenticado, 403 si no tiene permisos
		"""
		print(f"🔐 [PermissionChecker] Path: {request.url.path}")
		print(f"🔐 [PermissionChecker] Required permissions: {permissions}")

		# Validar que el usuario esté autenticado
		if not hasattr(request, "user") or not request.user:
			raise HTTPException(
				status_code=status.HTTP_401_UNAUTHORIZED,
				detail={
					"error_code": "UNAUTHORIZED",
					"message": "Authentication required for this endpoint",
					"required_permissions": list(permissions),
				},
				headers={"WWW-Authenticate": "Bearer"},
			)

		if isinstance(request.user, UnauthenticatedUser):
			raise HTTPException(
				status_code=status.HTTP_401_UNAUTHORIZED,
				detail={
					"error_code": "UNAUTHORIZED",
					"message": "Authentication required for this endpoint",
					"required_permissions": list(permissions),
				},
				headers={"WWW-Authenticate": "Bearer"},
			)

		# Obtener permisos del usuario
		user_permissions = _get_user_permissions(request)
		print(f"🔐 [PermissionChecker] User permissions: {user_permissions}")

		# Validar permisos
		missing = [p for p in permissions if p not in user_permissions]

		if missing:
			raise HTTPException(
				status_code=status.HTTP_403_FORBIDDEN,
				detail={
					"error_code": "FORBIDDEN",
					"message": f"Missing required permissions: {', '.join(missing)}",
					"required_permissions": list(permissions),
					"missing_permissions": missing,
				},
			)

		print("✅ [PermissionChecker] Access granted")

	return permission_checker


def _get_user_permissions(request: Request) -> List[str]:
	"""
	Obtiene la lista de permisos del usuario desde request.user.

	El usuario ya fue autenticado por AuthenticationMiddleware y sus
	permisos fueron cargados en el método authenticate() de AuthBackend.

	Args:
		request: Request con el usuario autenticado

	Returns:
		Lista de permisos del usuario (tokens)
	"""
	if not hasattr(request.user, "permissions"):
		return []

	permissions = request.user.permissions
	if permissions is None:
		return []

	return permissions
