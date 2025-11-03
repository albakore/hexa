from typing import Dict, Any, Optional, TypeVar, Type, Callable, cast, overload
from abc import ABC, abstractmethod
from dependency_injector.providers import Factory, Singleton
from dependency_injector.wiring import Provide

T = TypeVar("T")


class ServiceLocator:
	"""
	Localizador de servicios para comunicación entre módulos.

	Soporta type-safe lookups usando Protocols.
	"""

	def __init__(self):
		self._services: Dict[str, Any] = {}
		self._factories: Dict[str, Callable[[], Any]] = {}
		self._type_hints: Dict[str, Type] = {}  # Para almacenar type hints

	def register_service(
		self, name: str, service: Any, type_hint: Optional[Type] = None
	) -> None:
		"""Registra un servicio con un type hint opcional para type checking"""
		self._services[name] = service
		if type_hint:
			self._type_hints[name] = type_hint

	def register_factory(
		self, name: str, factory: Callable[[], Any], type_hint: Optional[Type] = None
	) -> None:
		"""Registra una factory con un type hint opcional para type checking"""
		self._factories[name] = factory
		if type_hint:
			self._type_hints[name] = type_hint

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
		"""
		Obtiene un servicio tipado con type checking.

		Uso:
		    from shared.interfaces.service_protocols import UserServiceProtocol
		    user_service = service_locator.get_typed_service("user_service", UserServiceProtocol)
		    # user_service ahora tiene type: UserServiceProtocol
		"""
		service = self.get_service(name)
		if service:
			return cast(service_type, service)
		return None

	def get_typed_dependency(self, name: str, service_type: Type[T]) -> Callable[[], T]:
		"""
		Obtiene una dependency function para FastAPI con type hints.

		Uso:
		    from shared.interfaces.service_protocols import UserServiceProtocol
		    from fastapi import Depends

		    @router.get("/")
		    async def endpoint(
		        user_service: UserServiceProtocol = Depends(
		            service_locator.get_typed_dependency("user_service", UserServiceProtocol)
		        )
		    ):
		        # user_service tiene type: UserServiceProtocol
		        ...
		"""

		def wrapper() -> T:
			if name in self._services:
				service = self._services[name]
				if isinstance(service, Factory):
					return cast(T, service())
				return cast(T, service)

			if name in self._factories:
				return cast(T, self._factories[name]())

			raise ValueError(f"Service '{name}' not found")

		return wrapper

	def has_service(self, name: str) -> bool:
		"""Verifica si un servicio está disponible"""
		return name in self._services or name in self._factories

	def clear(self) -> None:
		"""Limpia todos los servicios registrados"""
		self._services.clear()
		self._factories.clear()


# Instancia global del localizador de servicios
service_locator = ServiceLocator()
