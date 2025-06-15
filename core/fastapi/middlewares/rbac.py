from dependency_injector.wiring import inject
from starlette.authentication import AuthCredentials
from starlette.requests import Request
from starlette.types import ASGIApp, Receive, Scope, Send

from core.fastapi.middlewares.authentication import CurrentUser, User
class RBACMiddleware:
	def __init__(self, app: ASGIApp) -> None:
		self.app = app

	async def __call__(self, scope, receive, send):
		request = Request(scope, receive=receive)

		user : User | None = getattr(request, "user", None)
		auth : AuthCredentials = getattr(request, "auth")
		print("👤 Usuario desde middleware:", user)
		print("👤 Auth:", auth.scopes)

		# También puede chequear si está autenticado
		if user and user.is_authenticated:
			print("✅ Usuario autenticado:", user.id)

			print(user.nickname)


		await self.app(scope, receive, send)
