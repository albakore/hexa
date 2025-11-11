from dataclasses import dataclass
from typing import Sequence
from core.db import Transactional
from modules.provider.application.exception import ProviderNotFoundException
from modules.provider.domain.command import CreateProviderCommand
from modules.provider.domain.entity.provider import Provider
from modules.provider.domain.repository.provider import ProviderRepository
from modules.provider.domain.usecase.provider import (
	ProviderUseCaseFactory,
	UpdateProviderCommand,
)


@dataclass
class ProviderService:
	provider_repository: ProviderRepository

	def __post_init__(self):
		self.provider_usecase = ProviderUseCaseFactory(self.provider_repository)

	async def get_all_providers(
		self, limit: int = 20, page: int = 0
	) -> list[Provider] | Sequence[Provider]:
		return await self.provider_usecase.get_all_providers(limit, page)

	async def get_provider_by_id(self, id_provider: int) -> Provider:
		provider = await self.provider_usecase.get_provider_by_id(id_provider)
		if not provider:
			raise ProviderNotFoundException
		return provider

	async def create_provider(self, command: CreateProviderCommand) -> Provider:
		return self.provider_usecase.create_provider(command)

	async def save_provider(self, provider: Provider):
		return await self.provider_usecase.save_provider(provider)

	async def delete_provider(self, id_provider: int):
		provider = await self.provider_usecase.get_provider_by_id(id_provider)
		if not provider:
			raise ProviderNotFoundException
		return await self.provider_usecase.delete_provider(provider)

	async def update_provider(self, command: UpdateProviderCommand):
		return await self.provider_usecase.update_provider(command)
