import os
import importlib
from fastapi import APIRouter, Depends, FastAPI, Request
from pprint import pprint
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from rich import print
from app.container import MainContainer
from core.exceptions.base import CustomException
from core.fastapi.dependencies.logging import Logging
from core.fastapi.middlewares import (
	AuthBackend,
	AuthenticationMiddleware,
	ResponseLogMiddleware,
	SQLAlchemyMiddleware,
	RBACMiddleware
)


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
			backend=AuthBackend(),
			on_error=on_auth_error,
		),
		Middleware(SQLAlchemyMiddleware),
		Middleware(RBACMiddleware),
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


def get_routes():
	routes = []
	for root, dirs, files in os.walk("app"):
		if "adapter/input/api" in root:
			path = root.replace("/", ".")
			module = importlib.import_module(path)

			if hasattr(module, "router"):
				print(module.router.tags)
				print(module.router.routes)
				routes.append(module.router)

	return routes


def init_routers(app_: FastAPI) -> None:
	container = MainContainer()

	app_.container = container  # type: ignore
	for route in get_routes():
		route: APIRouter
		app_.include_router(route)


def create_app() -> FastAPI:
	app_ = FastAPI(
		dependencies=[Depends(Logging)],
		middleware=make_middleware(),
		servers=[{
			"url":"http://127.0.0.1:8000", "description": "development"
		}]
	)
	init_routers(app_=app_)
	init_listeners(app_=app_)
	return app_


app = create_app()
