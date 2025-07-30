from app.server import app_route
from modules.server import modules_route
from shared.server import shared_route

routes_pack = [
	app_route,
	modules_route,
	shared_route
]