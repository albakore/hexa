from dependency_injector.providers import Container, Factory
from dependency_injector.containers import DeclarativeContainer, WiringConfiguration

from shared.file_storage.container import FileStorageContainer

class SharedContainer(DeclarativeContainer):
	wiring_config = WiringConfiguration(
		packages=["shared"],
		auto_wire=True
	)
	
	file_storage = Container(FileStorageContainer)