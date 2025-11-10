import asyncio
import importlib
import json
import os
from contextlib import asynccontextmanager
from pprint import pprint
from typing import List

from dependency_injector.wiring import Provide
from fastapi import APIRouter, Depends, FastAPI, Request
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from rich import print

import shared.interfaces.module_discovery
from core.config.settings import env
from core.exceptions.base import CustomException
from core.fastapi.dependencies.logging import Logging
from core.fastapi.dependencies.permission import (
	sync_permissions_to_db,
	system_permission,
)
from core.fastapi.middlewares import (
	AuthBackend,
	AuthenticationMiddleware,
	PermissionValidationMiddleware,
	ResponseLogMiddleware,
	SQLAlchemyMiddleware,
)
from shared.interfaces.module_registry import ModuleRegistry
from shared.interfaces.service_locator import service_locator


def custom_generate_unique_id(route: APIRoute):
	return f"{route.tags[0]}-{route.name}"


def generate_openapi_for_frontend(app_: FastAPI):
	@app_.get("/system/openapi_schema", tags=["System"])
	def get_backend_schema():
		openapi_content = app_.openapi()
		for path_data in openapi_content["paths"].values():
			for operation in path_data.values():
				tag = operation["tags"][0]
				operation_id = operation["operationId"]
				to_remove = f"{tag}-"
				new_operation_id = operation_id[len(to_remove) :]
				operation["operationId"] = new_operation_id
		return openapi_content


def init_routes_pack(app_: FastAPI):
	for route in ModuleRegistry().get_routes():
		app_.include_router(route)


# Instancia global del AuthBackend para acceder a las excepciones
_auth_backend: AuthBackend | None = None


def on_auth_error(request: Request, exc: Exception):
	"""
	Manejador de errores de autenticación.

	Intenta obtener la excepción específica del AuthBackend si está disponible,
	de lo contrario usa la excepción genérica proporcionada por Starlette.
	"""
	global _auth_backend

	# Intentar obtener la excepción específica del backend
	if _auth_backend and _auth_backend.last_exception:
		exc = _auth_backend.last_exception

	status_code, error_code, message = 401, None, str(exc)
	if isinstance(exc, CustomException):
		status_code = int(exc.code)
		error_code = exc.error_code
		message = exc.message

	return JSONResponse(
		status_code=status_code,
		content={"error_code": error_code, "message": message},
	)


def make_middleware() -> list[Middleware]:
	global _auth_backend

	# Crear instancia única del AuthBackend
	_auth_backend = AuthBackend(
		user_service=service_locator.get_dependency("auth_service")  # type: ignore
	)

	middleware = [
		Middleware(
			CORSMiddleware,
			allow_origins=["*"],
			allow_credentials=True,
			allow_methods=["*"],
			allow_headers=["*"],
		),
		Middleware(
			AuthenticationMiddleware,
			backend=_auth_backend,
			on_error=on_auth_error,  # type: ignore
		),
		# NOTA: Ya no usamos PermissionValidationMiddleware como middleware
		# Los permisos se validan con una dependency inyectada automáticamente por @require_permissions
		# Middleware(PermissionValidationMiddleware),
		Middleware(SQLAlchemyMiddleware),
		# Middleware(ResponseLogMiddleware),
	]
	return middleware


def init_listeners(app_: FastAPI) -> None:
	# Exception handler
	@app_.exception_handler(CustomException)
	async def custom_exception_handler(request: Request, exc: CustomException):
		return JSONResponse(
			status_code=exc.code,
			content={"error_code": exc.error_code, "message": exc.message},
		)

	# General Exception handler
	@app_.exception_handler(Exception)
	async def general_exception_handler(request: Request, exc: Exception):
		task_service = service_locator.get_service("celery_app")

		notificacion = {
			"sender": "slack",
			"notification": {"body": f"Este es un error | {exc}"},
		}

		task_service.send_task(
			"notification.send_notification_tasks",
			args=[notificacion],
			# countdown=30,
		)

		return JSONResponse(
			status_code=500,
			content={"message": exc.args},
		)


def init_containers(app_: FastAPI) -> None:
	...
	# container = CoreContainer()
	# app_.container = container  # type: ignore


def export_openapi(app_: FastAPI):
	schema = get_openapi(
		title=app_.title, version=app_.version, servers=app_.servers, routes=app_.routes
	)
	with open(env.OPENAPI_EXPORT_DIR, "w+") as f:
		json.dump(schema, f, indent=2)


@asynccontextmanager
async def lifespan(app_: FastAPI):
	# 🚀 Startup
	# Los módulos ya fueron descubiertos en create_app()
	# await sync_permissions_to_db()
	# await sync_modules_to_db()
	yield  # 👉 La app corre a partir de aquí

	# 🔚 Shutdown (opcional)
	print("🧹 Limpieza al cerrar FastAPI")


def create_app() -> FastAPI:
	# IMPORTANTE: Limpiar registros en caso de reload y luego descubrir módulos
	# Esto es necesario cuando uvicorn hace reload con --reload
	from shared.interfaces.module_registry import ModuleRegistry
	from shared.interfaces.service_locator import service_locator

	ModuleRegistry().clear()
	service_locator.clear()

	# IMPORTANTE: Registrar celery_app ANTES de descubrir módulos
	# Los containers de los módulos pueden necesitar celery_app durante su inicialización
	from core.celery.discovery import get_celery_app, register_celery_tasks

	print("📱 Registering celery_app...")
	service_locator.register_service("celery_app", get_celery_app())

	# Descubrir módulos DESPUÉS de registrar servicios base
	print("🔍 Discovering and registering modules...")
	from shared.interfaces.module_discovery import discover_modules

	discover_modules("modules", "module.py")

	# Registrar tasks de Celery DESPUÉS de descubrir módulos
	print("📝 Registering Celery tasks...")
	register_celery_tasks()
	print("✅ Modules and tasks registered\n")

	app_ = FastAPI(
		generate_unique_id_function=custom_generate_unique_id,
		dependencies=[Depends(Logging)],
		middleware=make_middleware(),
		lifespan=lifespan,
		root_path=env.BACKEND_PATH,
		servers=[{"url": "http://localhost:8000", "description": "development"}],
		swagger_ui_parameters={
			"filter": True,
			"syntaxHighlight": {"activated": True, "theme": "monokai"},
			"requestSnippetsEnabled": True,
			"requestSnippets": {
				"generators": {
					"curl_bash": {"title": "cURL (bash)", "syntax": "bash"},
					"curl_powershell": {
						"title": "cURL (PowerShell)",
						"syntax": "powershell",
					},
					"curl_cmd": {"title": "cURL (CMD)", "syntax": "bash"},
					"node_native": {
						"title": "Node.js (Native)",
						"syntax": "javascript",
					},
					"python": {"title": "Python", "syntax": "python"},
				},
				"defaultExpanded": True,
				"languages": None,
				# e.g. only show curl bash = ["curl_bash"]
			},
		},
	)
	init_containers(app_=app_)
	init_routes_pack(app_=app_)
	# init_routers(app_=app_)
	init_listeners(app_=app_)
	export_openapi(app_=app_)
	generate_openapi_for_frontend(app_=app_)
	app_.include_router(system_permission)
	# app_.include_router(system_modules)
	return app_


app = create_app()
