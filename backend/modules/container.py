from dependency_injector.providers import Container, Factory
from dependency_injector.containers import DeclarativeContainer, WiringConfiguration

from modules.yiqi_erp.container import YiqiContainer
from modules.provider.container import ProviderContainer

class ModuleContainer(DeclarativeContainer):
	wiring_config = WiringConfiguration(
		packages=["modules"],
		auto_wire=True
	)
	
	provider = Container(ProviderContainer)
	yiqi_erp = Container(YiqiContainer)