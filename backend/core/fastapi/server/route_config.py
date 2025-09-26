from shared.server import shared_route
from shared.interfaces.module_registry import module_registry

# Importar módulos para auto-registro
import modules

# Obtener rutas de módulos registrados
module_routes = module_registry.get_routes()

routes_pack = [shared_route, *module_routes]
