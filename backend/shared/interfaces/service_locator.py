from typing import Dict, Any, Optional, TypeVar, Type, Callable
from abc import ABC, abstractmethod
from dependency_injector.providers import Factory

T = TypeVar("T")


class ServiceLocator:
	"""Localizador de servicios para comunicación entre módulos"""

	def __init__(self):
		self._services: Dict[str, Any] = {}
		self._factories: Dict[str, Callable[[], Any]] = {}

	def register_service(self, name: str, service: Any) -> None:
		self._services[name] = service

	def register_factory(self, name: str, factory: Callable[[], Any]) -> None:
		self._factories[name] = factory

	def get_service(self, name: str) -> Any:
		"""Obtiene un servicio resuelto para uso normal"""
		if name in self._services:
			service = self._services[name]
			if isinstance(service, Factory):
				return service()
			return service

		if name in self._factories:
			service = self._factories[name]()
			self._services[name] = service
			return service

		return None

	def get_dependency(self, name: str) -> Callable:
		"""Obtiene una función para usar con FastAPI Depends"""

		def wrapper():
			if name in self._services:
				service = self._services[name]
				if isinstance(service, Factory):
					return service()
				return service

			if name in self._factories:
				return self._factories[name]

			return None

		return wrapper

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
