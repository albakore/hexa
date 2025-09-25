from app.server import app_route
from modules.server import modules_route
from shared.server import shared_route
from shared.interfaces.module_registry import module_registry

# Importar módulos para auto-registro
import modules

# Obtener rutas de módulos registrados
module_routes = module_registry.get_routes()
print(module_routes)
routes_pack = [
	*module_routes
	# app_route,
	# modules_route,
	# shared_route
]
