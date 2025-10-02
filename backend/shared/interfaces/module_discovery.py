"""
Sistema simplificado de auto-registro
"""

from pathlib import Path
import importlib.util

from shared.interfaces.module_registry import ModuleInterface, ModuleRegistry


def auto_register_module_services():
	"""Auto-registra modulos"""

	modules_path = Path("modules")
	module_count = 0

	for module_dir in modules_path.iterdir():
		if module_dir.is_dir() and not module_dir.name.startswith("_"):
			module_file = module_dir / "module.py"
			if module_file.exists():
				module_count += 1
				try:
					module_path = str(module_file.with_suffix("")).replace("/", ".")
					module = importlib.import_module(module_path)

					for attr_name in dir(module):
						module_subclass = getattr(module, attr_name)

						if (
							isinstance(module_subclass, type)
							and issubclass(module_subclass, ModuleInterface)
							and module_subclass != ModuleInterface
						):
							ModuleRegistry().register(module_subclass())
							print(ModuleRegistry().get_routes())
							print(f"✅ {module_dir.name} module available")
							break
				except ImportError as e:
					print("Error import:", e)
					continue

	print(f"📦 Found {module_count} modules")


auto_register_module_services()
