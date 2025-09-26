from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from dependency_injector.containers import DeclarativeContainer


class ModuleInterface(ABC):
	"""Interface que deben implementar todos los módulos"""

	@property
	@abstractmethod
	def name(self) -> str:
		"""Nombre único del módulo"""
		pass

	@property
	@abstractmethod
	def container(self) -> DeclarativeContainer:
		"""Container de dependencias del módulo"""
		pass

	@property
	@abstractmethod
	def routes(self) -> Optional[Any]:
		"""Rutas del módulo (APIRouter)"""
		pass


class ModuleRegistry:
	"""Registro centralizado de módulos desacoplados"""

	def __init__(self):
		self._modules: Dict[str, ModuleInterface] = {}

	def register(self, module: ModuleInterface) -> None:
		"""Registra un módulo en el sistema"""
		if module.name in self._modules:
			raise ValueError(f"Module {module.name} already registered")
		self._modules[module.name] = module

	def get_module(self, name: str) -> Optional[ModuleInterface]:
		"""Obtiene un módulo por nombre"""
		return self._modules.get(name)

	def get_all_modules(self) -> Dict[str, ModuleInterface]:
		"""Obtiene todos los módulos registrados"""
		return self._modules.copy()

	def get_containers(self) -> Dict[str, DeclarativeContainer]:
		"""Obtiene todos los containers de los módulos"""
		return {name: module.container for name, module in self._modules.items()}

	def get_routes(self) -> list:
		"""Obtiene todas las rutas de los módulos"""
		routes = []
		for module in self._modules.values():
			if module.routes:
				routes.append(module.routes)
		return routes


# Instancia global del registro
module_registry = ModuleRegistry()
