from typing import List, Sequence
from modules.module.domain.entity.module import Module
from dataclasses import dataclass
from modules.module.domain.repository.module import AppModuleRepository


@dataclass
class GetModuleListUseCase:
	module_repository: AppModuleRepository

	async def __call__(
		self, limit: int = 20, page: int = 0
	) -> List[Module] | Sequence[Module]:
		return await self.module_repository.get_module_list(limit, page)


@dataclass
class GetModulesByIdsUseCase:
	module_repository: AppModuleRepository

	async def __call__(self, id_list: list[int]) -> List[Module] | Sequence[Module]:
		return await self.module_repository.get_modules_by_ids(ids=id_list)


@dataclass
class GetModulesByTokenNameUseCase:
	module_repository: AppModuleRepository

	async def __call__(
		self, token_name_list: list[str]
	) -> List[Module] | Sequence[Module]:
		return await self.module_repository.get_modules_by_token_name(
			token_name_list=token_name_list
		)


@dataclass
class ModuleUseCaseFactory:
	module_repository: AppModuleRepository

	def __post_init__(self):
		self.get_module_list = GetModuleListUseCase(self.module_repository)
		self.get_module_by_ids = GetModulesByIdsUseCase(self.module_repository)
		self.get_modules_by_token_name = GetModulesByTokenNameUseCase(
			self.module_repository
		)
