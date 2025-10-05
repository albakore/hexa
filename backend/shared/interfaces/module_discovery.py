"""
Sistema simplificado de auto-registro
"""

from pathlib import Path
import importlib.util
from types import ModuleType
from typing import Any

from shared.interfaces.service_locator import service_locator
from shared.interfaces.module_registry import ModuleInterface, ModuleRegistry


def eval_module_is_dir(path: Path) -> bool:
	return path.is_dir() and not path.name.startswith("_")


def module_exists(path: Path) -> bool:
	return path.exists()


def convert_path_to_pythonpath(path: Path) -> str:
	return str(path.with_suffix("")).replace("/", ".")


def import_python_module(python_path: str) -> ModuleType | None:
	try:
		print(python_path)
		return importlib.import_module(python_path)
	except ImportError as e:
		print("❌ Error import:", e, "path:", e.path)
		return None


def extract_attributes_from_module(module: ModuleType) -> list[str]:
	return dir(module)


def is_subclass_of(subclass_attribute: Any, parent_class: type) -> bool:
	return (
		isinstance(subclass_attribute, type)
		and issubclass(subclass_attribute, parent_class)
		and subclass_attribute != parent_class
	)


def registre_module(subclass_attribute: type[ModuleInterface]):
	subclass_module = subclass_attribute()
	ModuleRegistry().register(subclass_module)
	print(f"✅ Found {subclass_module.name} module")
	for name, service in subclass_module.service.items():
		service_locator.register_service(name, service)
		print(f" ˪💼 '{name}' service installed.")


def discover_modules(root_dir: str, module_filename: str):
	"""Auto-registra modulos"""

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
		module_attributes = extract_attributes_from_module(module)
		for attribute in module_attributes:
			module_subclass: type[ModuleInterface] = getattr(module, attribute)
			if is_subclass_of(module_subclass, ModuleInterface):
				registre_module(module_subclass)
				module_count += 1

	print(f"📦 Total {module_count} modules installed")


discover_modules("modules", "module.py")
