from dependency_injector.providers import Container, Factory
from dependency_injector.containers import DeclarativeContainer, WiringConfiguration

from app.container import SystemContainer
from modules.container import ModuleContainer
from shared.container import SharedContainer

class CoreContainer(DeclarativeContainer):
	wiring_config = WiringConfiguration(packages=["app","modules","shared"], auto_wire=True)

	system = Container(SystemContainer)
	module = Container(ModuleContainer)
	shared = Container(SharedContainer)
