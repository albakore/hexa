"""
Middleware de FastAPI para auditoría automática

Este middleware configura automáticamente el contexto de auditoría
en cada request HTTP.
"""

from starlette.types import ASGIApp, Receive, Scope, Send
from starlette.requests import Request

from core.audit.context import set_audit_context, clear_audit_context


class AuditMiddleware:
	"""
	Middleware que configura el contexto de auditoría para cada request.

	Captura automáticamente:
	- Usuario autenticado (si existe en request.user)
	- Dirección IP del cliente
	- User agent
	- Endpoint de la API
	- Método HTTP

	Este middleware debe ejecutarse DESPUÉS de AuthenticationMiddleware
	para que request.user esté disponible.

	Paths excluidos por defecto:
	- /docs, /redoc, /openapi.json (Swagger/OpenAPI)
	- /health, /healthz, /ping (Health checks)
	- /metrics (Prometheus metrics)
	- Paths estáticos (/static, /assets)

	Uso en core/fastapi/server/__init__.py:
		middleware = [
			Middleware(CORSMiddleware, ...),
			Middleware(AuthenticationMiddleware, ...),
			Middleware(AuditMiddleware, exclude_paths=['/custom/exclude']),
			Middleware(SQLAlchemyMiddleware),
		]
	"""

	def __init__(
		self,
		app: ASGIApp,
		exclude_paths: list[str] | None = None
	) -> None:
		self.app = app

		# Paths excluidos por defecto
		self.default_exclude_paths = [
			'/docs',
			'/redoc',
			'/openapi.json',
			'/system/openapi_schema',
			'/health',
			'/healthz',
			'/ping',
			'/metrics',
		]

		# Paths adicionales proporcionados por el usuario
		self.exclude_paths = self.default_exclude_paths + (exclude_paths or [])

		# Prefijos a ignorar
		self.exclude_prefixes = [
			'/static',
			'/assets',
		]

	def _should_exclude_path(self, path: str) -> bool:
		"""
		Determina si un path debe ser excluido de la auditoría.

		Args:
			path: Path del request

		Returns:
			True si debe ser excluido, False en caso contrario
		"""
		# Verificar paths exactos
		if path in self.exclude_paths:
			return True

		# Verificar prefijos
		for prefix in self.exclude_prefixes:
			if path.startswith(prefix):
				return True

		return False

	async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
		"""
		Procesa el request configurando el contexto de auditoría.

		Args:
			scope: ASGI scope
			receive: ASGI receive
			send: ASGI send
		"""
		# Solo procesar requests HTTP
		if scope["type"] != "http":
			await self.app(scope, receive, send)
			return

		# Crear request para acceder a sus propiedades
		request = Request(scope, receive, send)

		# Verificar si el path debe ser excluido
		if self._should_exclude_path(request.url.path):
			# Saltar auditoría para este endpoint
			await self.app(scope, receive, send)
			return

		# Obtener usuario autenticado si existe
		# El AuthenticationMiddleware establece request.user
		user_id = None
		user_email = None

		if hasattr(request, "user") and request.user and request.user.is_authenticated:
			# El usuario está en request.user (no en request.state.user)
			user_id = getattr(request.user, "id", None)
			user_email = getattr(request.user, "email", None)

		# Obtener información del cliente
		client_host = None
		if request.client:
			client_host = request.client.host

		# Configurar el contexto de auditoría
		set_audit_context(
			user_id=user_id,
			user_email=user_email,
			ip_address=client_host,
			user_agent=request.headers.get("user-agent"),
			endpoint=request.url.path,
			method=request.method
		)

		try:
			# Procesar el request
			await self.app(scope, receive, send)
		except Exception as e:
			# Re-lanzar la excepción después de limpiar
			raise e
		finally:
			# Limpiar el contexto al finalizar el request
			clear_audit_context()
