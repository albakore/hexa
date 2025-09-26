from fastapi import APIRouter
from core.fastapi.server.route_helpers import get_routes, set_routes_to_app

routes = get_routes("shared")
shared_route = APIRouter()
set_routes_to_app(shared_route, routes)
