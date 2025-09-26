from dependency_injector.providers import Container, Factory, Singleton
from dependency_injector.containers import DeclarativeContainer, WiringConfiguration

from shared.file_storage.container import FileStorageContainer
from shared.interfaces.module_registry import ModuleRegistry
from shared.interfaces.events import EventBus
from shared.interfaces.service_locator import ServiceLocator


class SharedContainer(DeclarativeContainer):
	wiring_config = WiringConfiguration(packages=["shared"], auto_wire=True)

	file_storage = Container(FileStorageContainer)
	module_registry = Singleton(ModuleRegistry)
	event_bus = Singleton(EventBus)
	service_locator = Singleton(ServiceLocator)
