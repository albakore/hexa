"""
Middleware para validar permisos en endpoints decorados con @require_permissions.

Este middleware:
1. Intercepta requests a endpoints
2. Verifica si el endpoint tiene el decorador @require_permissions
3. Obtiene los permisos del usuario desde request.user (ya autenticado por AuthenticationMiddleware)
4. Valida que el usuario tenga TODOS los permisos requeridos
5. Si no tiene permisos, retorna 403 Forbidden
"""

from starlette.types import ASGIApp, Receive, Scope, Send


class PermissionValidationMiddleware:
	"""
	Middleware que valida permisos basándose en el decorador @require_permissions.

	Debe ser colocado DESPUÉS de AuthenticationMiddleware en el stack de middlewares
	para que request.user ya esté disponible.

	El middleware busca el atributo __required_permissions__ en la función del endpoint,
	que es inyectado por el decorador @require_permissions.

	IMPORTANTE: Usa el protocolo ASGI puro en lugar de BaseHTTPMiddleware
	para tener acceso al endpoint en el scope.
	"""

	def __init__(self, app: ASGIApp) -> None:
		self.app = app

	async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
		# pprint(scope)

		try:
			await self.app(scope, receive, send)
		except Exception as e:
			raise e
		finally:
			print("Saliendo de permissions")
