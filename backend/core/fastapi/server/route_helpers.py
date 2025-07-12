
import importlib
import os
from typing import List

from fastapi import APIRouter


def get_routes(folder_root_name : str = "app"):
	routes = []
	for root, dirs, files in os.walk(folder_root_name):
		if "adapter/input/api" in root:
			path = root.replace("/", ".")
			module = importlib.import_module(path)

			if hasattr(module, "router"):
				# print(module.router.tags)
				# print(module.router.routes)
				routes.append(module.router)

	return routes

def set_routes_to_app(app_or_route : APIRouter, routes : List[APIRouter]):
	for route in routes:
		app_or_route.include_router(route)
