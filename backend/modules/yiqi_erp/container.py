from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Singleton, Factory, Configuration

from modules.yiqi_erp.application.service.yiqi import YiqiService

from modules.yiqi_erp.adapter.output.api.http_client import YiqiHttpClient
from core.config.settings import env
from modules.yiqi_erp.adapter.output.api.yiqi_rest import YiqiApiRepository


class YiqiContainer(DeclarativeContainer):
	wiring_config = WiringConfiguration(packages=["."], auto_wire=True)

	config = Configuration(pydantic_settings=[env])

	client = Singleton(
		YiqiHttpClient,
		base_url=config.YIQI_BASE_URL,
		api_key=config.YIQI_API_TOKEN,
		api_timeout=200.0,
	)

	repository = Factory(
		YiqiApiRepository,
		client=client,
	)

	service = Factory(YiqiService, yiqi_repository=repository)

	async def shutdown(self):
		await self.client().close()
