from typing import Sequence
from modules.provider.domain.entity.provider import Provider
from abc import ABC, abstractmethod


class ProviderRepository(ABC):
	@abstractmethod
	async def get_all_providers(
		self, limit: int = 12, page: int = 0
	) -> list[Provider] | Sequence[Provider]: ...

	@abstractmethod
	async def get_provider_by_id(self, id_provider: int) -> Provider | None: ...

	@abstractmethod
	async def save(self, provider: Provider) -> Provider | None: ...

	@abstractmethod
	async def delete(self, provider: Provider): ...
