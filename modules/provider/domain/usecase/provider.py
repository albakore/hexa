
from abc import ABC, abstractmethod

from modules.provider.domain.command import CreateProviderCommand
from modules.provider.domain.entity.provider import Provider


class ProviderUseCase(ABC):
	
	@abstractmethod
	async def get_all_providers(self) -> list[Provider]: ...

	@abstractmethod
	async def get_provider_by_id(self, id_provider : int) -> Provider | None : ...

	@abstractmethod
	async def create_provider(self, command : CreateProviderCommand) -> Provider: ...

	@abstractmethod
	async def save(self, provider: Provider): ...

	@abstractmethod
	async def delete(self, provider: Provider): ...