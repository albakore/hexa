"""
Sistema simplificado de auto-registro de módulos
Trabaja con variables y funciones simples en lugar de clases
"""

import importlib.util
from pathlib import Path
from types import ModuleType

from shared.interfaces.module_registry import ModuleRegistry
from shared.interfaces.service_locator import service_locator


def eval_module_is_dir(path: Path) -> bool:
	return path.is_dir() and not path.name.startswith("_")


def module_exists(path: Path) -> bool:
	return path.exists()


def convert_path_to_pythonpath(path: Path) -> str:
	return str(path.with_suffix("")).replace("/", ".")


def import_python_module(python_path: str) -> ModuleType | None:
	try:
		# print(python_path)
		return importlib.import_module(python_path)
	except ImportError as e:
		print("❌ Error import:", e, "path:", e.path)
		return None


def register_module(module: ModuleType):
	"""
	Registra un módulo simple que contiene variables directas:
	- name: str
	- container: DeclarativeContainer
	- service: Dict[str, object]
	- routes: APIRouter (opcional)
	"""
	module_name = getattr(module, "name", None)
	if not module_name:
		print(f"⚠️  Module {module.__name__} doesn't have 'name' attribute")
		return False

	module_container = getattr(module, "container", None)
	module_services = getattr(module, "service", {})
	module_routes = getattr(module, "routes", None)

	# Registrar en ModuleRegistry
	ModuleRegistry().register(
		name=module_name,
		container=module_container,
		service=module_services,
		routes=module_routes,
	)
	# Registrar servicios en service_locator
	for name, service in module_services.items():
		service_locator.register_service(name, service)

	return True


def discover_modules(root_dir: str, module_filename: str):
	"""Auto-registra módulos escaneando archivos module.py"""

	modules_path = Path(root_dir)
	module_count = 0

	for module_dir in modules_path.iterdir():
		if not eval_module_is_dir(module_dir):
			continue

		module_file = module_dir / module_filename
		if not module_exists(module_file):
			continue

		module_path = convert_path_to_pythonpath(module_file)
		module = import_python_module(module_path)

		if not module:
			continue

		if register_module(module):
			module_count += 1

	# Mostrar resumen detallado
	_print_module_summary()


def discover_permissions(root_dir: str):
	"""
	Auto-descubre e importa archivos permissions.py de todos los módulos.

	Esto asegura que las clases PermissionGroup se registren en PERMISSIONS_REGISTRY
	antes de sincronizar permisos con la base de datos.
	"""
	modules_path = Path(root_dir)
	permissions_count = 0

	print("🔍 Discovering permission files...")
	print("-" * 70)

	for module_dir in modules_path.iterdir():
		if not eval_module_is_dir(module_dir):
			continue

		permissions_file = module_dir / "permissions.py"
		if not module_exists(permissions_file):
			continue

		module_path = convert_path_to_pythonpath(permissions_file)
		module = import_python_module(module_path)

		if module:
			permissions_count += 1
			print(f"✅ Loaded permissions from '{module_dir.name}' module")

	# Mostrar resumen
	_print_permissions_summary(permissions_count)


def _print_module_summary():
	"""Imprime un resumen detallado de los módulos, containers, rutas y servicios registrados"""
	registry = ModuleRegistry()
	modules = registry.get_all_modules()
	containers = registry.get_containers()
	routes = registry.get_routes()

	print("=" * 70)
	print(f"📦 RESUMEN DE MÓDULOS REGISTRADOS")
	print("=" * 70)
	print()

	# Módulos
	print(f"✅ Total de módulos: {len(modules)}")
	for name in sorted(modules.keys()):
		module = modules[name]
		has_routes = "✓" if module.get("routes") else "✗"
		has_container = "✓" if module.get("container") else "✗"
		print(
			f"   • {name:25s} [Type: ModuleData     ] "
			f"Routes: {has_routes}  Container: {has_container}"
		)

	print()
	print("-" * 70)

	# Containers
	print(f"📦 Containers registrados: {len(containers)}")
	for name in sorted(containers.keys()):
		print(f"   • {name}")

	print()
	print("-" * 70)

	# Rutas
	print(f"🛣️  Routers registrados: {len(routes)}")

	print()
	print("-" * 70)

	# Servicios
	services = service_locator._services
	print(f"💼 Servicios en service_locator: {len(services)}")
	for name in sorted(services.keys()):
		service_obj = services[name]
		service_type = type(service_obj).__name__
		print(f"   • {name:45s} [{service_type}]")

	print()
	print("=" * 70)
	print("✅ Descubrimiento de módulos completado exitosamente")
	print("=" * 70)
	print()


def _print_permissions_summary(permissions_count: int):
	"""Imprime un resumen del descubrimiento de permisos"""
	print()
	print("=" * 70)
	print(f"🔐 RESUMEN DE PERMISOS")
	print("=" * 70)
	print()
	print(f"✅ Total de archivos de permisos cargados: {permissions_count}")
	print()
	print("=" * 70)
	print("✅ Descubrimiento de permisos completado exitosamente")
	print("=" * 70)
	print()


# Note: discover_modules() debe ser llamado explícitamente:
# - En FastAPI: core/fastapi/server.py durante lifespan
# - En Celery: hexa/__main__.py en el comando celery-apps
# No se llama automáticamente aquí para evitar doble registro
