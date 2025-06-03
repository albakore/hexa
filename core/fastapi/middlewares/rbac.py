from starlette.types import ASGIApp, Receive, Scope, Send
class RBACMiddleware:
	def __init__(self, app: ASGIApp) -> None:
		self.app = app

	async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
		print("Ingresa al RBAC Middleware")
		print(scope.items())
		try:
			await self.app(scope, receive, send)
		except Exception as e:
			raise e
		finally:
			print("Sale del RBAC Middleware")