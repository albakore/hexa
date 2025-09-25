from fastapi import APIRouter
from shared.interfaces.module_registry import module_registry
from shared.interfaces.service_registry import auto_register_module_services
from core.fastapi.server.route_helpers import get_routes, set_routes_to_app

auto_register_module_services()
routes = get_routes("shared")
shared_route = APIRouter()
set_routes_to_app(shared_route, routes)
