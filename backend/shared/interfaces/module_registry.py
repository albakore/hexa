from abc import ABC, abstractmethod
import threading
from typing import Dict, Any, Optional, TypeVar, TypedDict
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Object

T = TypeVar("T")


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
	def service(self) -> Dict[str, object]:
		pass

	@property
	@abstractmethod
	def routes(self) -> Optional[Any]:
		"""Rutas del módulo (APIRouter)"""
		pass


class ModuleRegistry:
	"""Registro centralizado de módulos desacoplados"""

	_instance = None
	_lock = threading.Lock()

	def __new__(cls):
		if not cls._instance:  # This is the only difference
			with cls._lock:
				if not cls._instance:
					cls._instance = super().__new__(cls)
		return cls._instance

	def __init__(self):
		if not hasattr(self, "_modules"):
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
			print(module.routes)
			if module.routes:
				routes.append(module.routes)
		return routes
