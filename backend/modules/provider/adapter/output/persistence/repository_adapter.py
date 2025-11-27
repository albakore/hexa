from typing import List, Sequence

from modules.provider.domain.command import SearchProviderCommand
from modules.provider.domain.entity.provider import Provider
from modules.provider.domain.repository.provider import ProviderRepository


class ProviderRepositoryAdapter(ProviderRepository):
	def __init__(self, provider_repository: ProviderRepository):
		self.provider_repository = provider_repository

	async def get_all_providers(
		self, limit: int = 5000, page: int = 0
	) -> list[Provider] | Sequence[Provider]:
		return await self.provider_repository.get_all_providers(limit, page)

	async def get_provider_by_id(self, id_provider: int) -> Provider | None:
		return await self.provider_repository.get_provider_by_id(id_provider)

	async def save(self, provider: Provider) -> Provider | None:
		return await self.provider_repository.save(provider)

	async def delete(self, provider: Provider):
		return await self.provider_repository.delete(provider)

	async def search_providers(
		self, command: SearchProviderCommand
	) -> tuple[List[Provider] | Sequence[Provider], int]:
		return await self.provider_repository.search_providers(command)
