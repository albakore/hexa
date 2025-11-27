"""
Registro centralizado de módulos
Sistema simplificado usando diccionarios tipados en lugar de clases
"""

import threading
from typing import Any, Dict, Optional, TypedDict

from dependency_injector.containers import DeclarativeContainer


class ModuleData(TypedDict, total=False):
	"""Estructura de datos de un módulo registrado"""

	name: str  # Requerido
	container: Optional[DeclarativeContainer]  # Opcional
	service: Dict[str, object]  # Requerido
	routes: Optional[Any]  # Opcional


class ModuleRegistry:
	"""
	Registro centralizado de módulos (Singleton)

	Gestiona el registro y acceso a módulos de la aplicación.
	Cada módulo es representado por un diccionario con:
	- name: Identificador único del módulo
	- container: Container de Dependency Injection
	- service: Servicios expuestos al service_locator
	- routes: APIRouter con las rutas del módulo
	"""

	_instance: Optional["ModuleRegistry"] = None
	_lock = threading.Lock()

	def __new__(cls) -> "ModuleRegistry":
		if not cls._instance:
			with cls._lock:
				if not cls._instance:
					cls._instance = super().__new__(cls)
		return cls._instance

	def __init__(self):
		if not hasattr(self, "_modules"):
			self._modules: Dict[str, ModuleData] = {}

	def register(
		self,
		name: str,
		container: Optional[DeclarativeContainer] = None,
		service: Optional[Dict[str, object]] = None,
		routes: Optional[Any] = None,
	) -> None:
		"""
		Registra un nuevo módulo en el sistema

		Args:
			name: Identificador único del módulo
			container: Container de Dependency Injection (opcional)
			service: Diccionario de servicios expuestos (opcional, default {})
			routes: APIRouter con las rutas del módulo (opcional)

		Raises:
			ValueError: Si el módulo ya está registrado
		"""
		if name in self._modules:
			raise ValueError(f"Module '{name}' is already registered")

		module_data: ModuleData = {
			"name": name,
			"container": container,
			"service": service or {},
			"routes": routes,
		}

		self._modules[name] = module_data

	def get_module(self, name: str) -> Optional[ModuleData]:
		"""
		Obtiene un módulo por su nombre

		Args:
			name: Nombre del módulo

		Returns:
			ModuleData si existe, None si no existe
		"""
		return self._modules.get(name)

	def get_all_modules(self) -> Dict[str, ModuleData]:
		"""
		Obtiene todos los módulos registrados

		Returns:
			Diccionario con todos los módulos (copia)
		"""
		return self._modules.copy()

	def get_containers(self) -> Dict[str, DeclarativeContainer]:
		"""
		Obtiene todos los containers de los módulos

		Returns:
			Diccionario con nombre del módulo como clave y container como valor
		"""
		containers = {}
		for name, module in self._modules.items():
			container = module.get("container")
			if container:
				containers[name] = container
		return containers

	def get_routes(self) -> list[Any]:
		"""
		Obtiene todas las rutas de los módulos

		Returns:
			Lista de APIRouters de todos los módulos que tienen rutas
		"""
		routes = []
		for module in self._modules.values():
			route = module.get("routes")
			if route:
				routes.append(route)
		return routes

	def has_module(self, name: str) -> bool:
		"""
		Verifica si un módulo está registrado

		Args:
			name: Nombre del módulo

		Returns:
			True si el módulo existe, False si no
		"""
		return name in self._modules

	def get_module_names(self) -> list[str]:
		"""
		Obtiene los nombres de todos los módulos registrados

		Returns:
			Lista con los nombres de los módulos
		"""
		return list(self._modules.keys())

	def clear(self) -> None:
		"""Limpia todos los módulos registrados (útil para testing)"""
		self._modules.clear()

	def __len__(self) -> int:
		"""Retorna el número de módulos registrados"""
		return len(self._modules)

	def __contains__(self, name: str) -> bool:
		"""Permite usar 'nombre_modulo in registry'"""
		return name in self._modules

	def __repr__(self) -> str:
		"""Representación string del registro"""
		return f"ModuleRegistry(modules={len(self._modules)})"
