import os
import importlib
from fastapi import APIRouter, FastAPI
from pprint import pprint

from app.container import MainContainer

def get_routes():
	routes = []
	for root, dirs, files in os.walk("app"):
		if "adapter/input/api" in root:
			path = root.replace("/", ".")
			module = importlib.import_module(path)

			if hasattr(module, "router"):
				pprint(module.router.tags)
				pprint(module.router.routes)
				routes.append(module.router)

	return routes

def init_routers(app_: FastAPI) -> None:
	container = MainContainer()

	app_.container = container #type: ignore
	for route in get_routes():
		route : APIRouter
		app_.include_router(route)


def create_app() -> FastAPI:
	app_ = FastAPI()
	init_routers(app_=app_)
	return app_

app = create_app()
