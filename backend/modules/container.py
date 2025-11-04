from dependency_injector.providers import Configuration, Container, Factory
from dependency_injector.containers import DeclarativeContainer, WiringConfiguration

from modules.finance.container import FinanceContainer
from modules.yiqi_erp.container import YiqiContainer
from modules.provider.container import ProviderContainer
from modules.inventory.container import InventoryContainer
from core.config.settings import env

class ModuleContainer(DeclarativeContainer):
	wiring_config = WiringConfiguration(
		packages=["modules"],
		auto_wire=True
	)
	config = Configuration(pydantic_settings=[env])
	
	yiqi_erp = Container(YiqiContainer, config=config)
	provider = Container(ProviderContainer,yiqi_service=yiqi_erp.service)
	finance = Container(FinanceContainer)
	inventory = Container(InventoryContainer)