
from typing import Sequence
from core.db import Transactional
from modules.provider.domain.command import CreateProviderCommand
from modules.provider.domain.entity.provider import Provider
from modules.provider.domain.repository.provider import ProviderRepository
from modules.provider.domain.usecase.provider import ProviderUseCase


class ProviderService(ProviderUseCase):
	
	def __init__(self, provider_repository : ProviderRepository):
		self.provider_repository = provider_repository

	async def get_all_providers(self) -> list[Provider] | Sequence[Provider]:
		providers = await self.provider_repository.get_all_providers()
		return providers

	async def get_provider_by_id(self, id_provider: int) -> Provider | None:
		provider = await self.provider_repository.get_provider_by_id(id_provider)
		return provider

	async def create_provider(self, command: CreateProviderCommand) -> Provider:
		return Provider.model_validate(command)

	@Transactional()
	async def save(self, provider: Provider):
		await self.provider_repository.save(provider)

	@Transactional()
	async def delete(self, provider: Provider):
		await self.provider_repository.delete(provider)


	