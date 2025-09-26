"""
Container dinámico que auto-registra módulos
"""
from dependency_injector import containers
import importlib
from pathlib import Path


class CoreContainer(containers.DynamicContainer):
	"""Container dinámico que auto-registra módulos"""

	def __init__(self):
		super().__init__()
		self._auto_register_modules()

	def _auto_register_modules(self):
		"""Auto-registra todos los containers de módulos"""
		modules_path = Path("modules")

		for module_dir in modules_path.iterdir():
			if module_dir.is_dir() and not module_dir.name.startswith("_"):
				try:
					container_module = importlib.import_module(
						f"modules.{module_dir.name}.container"
					)

					# Buscar la clase Container en el módulo
					for attr_name in dir(container_module):
						attr = getattr(container_module, attr_name)
						if (
							isinstance(attr, type)
							and issubclass(attr, containers.DeclarativeContainer)
							and attr != containers.DeclarativeContainer
						):
							container_name = f"{module_dir.name}_container"
							self.set_provider(container_name, attr())
							break

				except ImportError:
					continue
