from typing import Dict, Any, Optional, TypeVar, Type, Callable
from abc import ABC, abstractmethod

T = TypeVar("T")


class ServiceLocator:
	"""Localizador de servicios para comunicación entre módulos"""

	def __init__(self):
		self._services: Dict[str, Any] = {}
		self._factories: Dict[str, Callable[[], Any]] = {}

	def register_service(self, name: str, service: Any) -> None:
		"""Registra un servicio por nombre"""
		self._services[name] = service

	def register_factory(self, name: str, factory: Callable[[], Any]) -> None:
		"""Registra una factory para crear servicios bajo demanda"""
		self._factories[name] = factory

	def get_service(self, name: str) -> Optional[T]:
		"""Obtiene un servicio por nombre"""
		if name in self._services:
			return self._services[name]

		if name in self._factories:
			service = self._factories[name]()
			self._services[name] = service  # Cache del servicio
			return service

		return None

	def get_typed_service(self, name: str, service_type: Type[T]) -> Optional[T]:
		"""Obtiene un servicio tipado"""
		service = self.get_service(name)
		if service and isinstance(service, service_type):
			return service
		return None

	def has_service(self, name: str) -> bool:
		"""Verifica si un servicio está disponible"""
		return name in self._services or name in self._factories

	def clear(self) -> None:
		"""Limpia todos los servicios registrados"""
		self._services.clear()
		self._factories.clear()


# Instancia global del localizador de servicios
service_locator = ServiceLocator()


# ServiceProvider removido - los módulos registran servicios directamente
