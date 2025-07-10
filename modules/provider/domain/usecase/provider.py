
from abc import ABC, abstractmethod
from dataclasses import dataclass

from core.db import Transactional
from modules.provider.domain.command import CreateProviderCommand
from modules.provider.domain.entity.provider import Provider
from modules.provider.domain.repository.provider import ProviderRepository


@dataclass
class GetAllProvidersUseCase:
	provider_repository : ProviderRepository

	async def __call__(self, limit: int = 20, page: int = 0) -> list[Provider]: ...


@dataclass
class GetProviderByIdUseCase:
	provider_repository : ProviderRepository

	async def __call__(self, id_provider : int) -> Provider | None : ...

@dataclass
class CreateProviderUseCase:
	provider_repository : ProviderRepository

	async def __call__(self, command : CreateProviderCommand) -> Provider: ...

@dataclass
class SaveProviderUseCase:
	provider_repository : ProviderRepository

	@Transactional()
	async def __call__(self, provider: Provider): ...


@dataclass
class DeleteProviderUseCase:
	provider_repository : ProviderRepository

	@Transactional()
	async def __call__(self, provider: Provider): ...



@dataclass
class ProviderUseCaseFactory:
	provider_repository : ProviderRepository

	def __post_init__(self):
		self.get_all_providers = GetAllProvidersUseCase(self.provider_repository)
		self.get_provider_by_id = GetProviderByIdUseCase(self.provider_repository)
		self.create_provider = CreateProviderUseCase(self.provider_repository)
		self.save_provider = SaveProviderUseCase(self.provider_repository)
		self.delete_provider = DeleteProviderUseCase(self.provider_repository)