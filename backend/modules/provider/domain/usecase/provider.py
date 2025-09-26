from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, Sequence

from modules.user.domain.entity import User
from modules.user.domain.repository.user import UserRepository
from core.db import Transactional
from modules.provider.application.exception import ProviderNotFoundException
from modules.provider.domain.command import CreateProviderCommand, UpdateProviderCommand
from modules.provider.domain.entity.provider import Provider
from modules.provider.domain.repository.provider import ProviderRepository


@dataclass
class GetAllProvidersUseCase:
	provider_repository: ProviderRepository

	async def __call__(
		self, limit: int = 20, page: int = 0
	) -> list[Provider] | Sequence[Provider]:
		return await self.provider_repository.get_all_providers(limit, page)


@dataclass
class GetProviderByIdUseCase:
	provider_repository: ProviderRepository

	async def __call__(self, id_provider: int) -> Provider | None:
		return await self.provider_repository.get_provider_by_id(id_provider)


@dataclass
class CreateProviderUseCase:
	provider_repository: ProviderRepository

	def __call__(self, command: CreateProviderCommand) -> Provider:
		return Provider.model_validate(command)


@dataclass
class SaveProviderUseCase:
	provider_repository: ProviderRepository

	@Transactional()
	async def __call__(self, provider: Provider):
		return await self.provider_repository.save(provider)


@dataclass
class UpdateProviderUseCase:
	provider_repository: ProviderRepository

	@Transactional()
	async def __call__(self, command: UpdateProviderCommand):
		provider = await self.provider_repository.get_provider_by_id(command.id)
		if not provider:
			raise ProviderNotFoundException
		provider.sqlmodel_update(command)
		return await self.provider_repository.save(provider)


@dataclass
class DeleteProviderUseCase:
	provider_repository: ProviderRepository

	@Transactional()
	async def __call__(self, provider: Provider):
		return await self.provider_repository.delete(provider)


@dataclass
class LinkUserToProviderUseCase:
	provider_repository: ProviderRepository
	user_repository: UserRepository

	@Transactional()
	async def __call__(self, user: User, provider: Provider):
		user.providers.append(provider)
		return await self.user_repository.save(user)


@dataclass
class ProviderUseCaseFactory:
	provider_repository: ProviderRepository

	def __post_init__(self):
		self.get_all_providers = GetAllProvidersUseCase(self.provider_repository)
		self.get_provider_by_id = GetProviderByIdUseCase(self.provider_repository)
		self.create_provider = CreateProviderUseCase(self.provider_repository)
		self.save_provider = SaveProviderUseCase(self.provider_repository)
		self.delete_provider = DeleteProviderUseCase(self.provider_repository)
		self.update_provider = UpdateProviderUseCase(self.provider_repository)
