import asyncio
from contextlib import asynccontextmanager
import json
import os
import importlib
from typing import List
from dependency_injector.wiring import Provide
from fastapi import APIRouter, Depends, FastAPI, Request
from pprint import pprint
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from rich import print
from app.container import SystemContainer
from core.exceptions.base import CustomException
from core.fastapi.dependencies.logging import Logging
from core.fastapi.middlewares import (
	AuthBackend,
	AuthenticationMiddleware,
	ResponseLogMiddleware,
	SQLAlchemyMiddleware
)
from core.config.settings import env
from core.fastapi.dependencies.permission import system_permission, sync_permissions_to_db
from .route_config import routes_pack
from .container_config import container_pack

def init_routes_pack(app_ : FastAPI):
	for route in routes_pack:
		app_.include_router(route)

def on_auth_error(request: Request, exc: Exception):
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
			backend=AuthBackend(auth_repository=SystemContainer.auth.repository_adapter()),
			on_error=on_auth_error, #type: ignore
		),
		Middleware(SQLAlchemyMiddleware),
		Middleware(ResponseLogMiddleware),
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

def init_containers(app_ : FastAPI) -> None:
	container = SystemContainer()
	app_.container = container  # type: ignore

def export_openapi(app_: FastAPI):
	schema = get_openapi(
			title=app_.title,
			version=app_.version,
			servers=app_.servers,
			routes=app_.routes
		)
	with open(env.OPENAPI_EXPORT_DIR, "w+") as f:
		json.dump(schema, f, indent=2)

@asynccontextmanager
async def lifespan(app_: FastAPI):
    # 🚀 Startup
    await sync_permissions_to_db()
    print("✅ Permisos sincronizados en base de datos")

    yield  # 👉 La app corre a partir de aquí

    # 🔚 Shutdown (opcional)
    print("🧹 Limpieza al cerrar FastAPI")

def create_app() -> FastAPI:
	app_ = FastAPI(
		dependencies=[Depends(Logging)],
		middleware=make_middleware(),
		lifespan=lifespan,
		root_path=env.BACKEND_PATH,
		servers=[{
			"url":"http://localhost:8000", "description": "development"
		}]
		
	)
	init_containers(app_=app_)
	init_routes_pack(app_=app_)
	# init_routers(app_=app_)
	init_listeners(app_=app_)
	export_openapi(app_=app_)
	app_.include_router(system_permission)
	return app_

app = create_app()