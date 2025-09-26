from typing import List, Sequence
from modules.app_module.domain.repository.module import AppModuleRepository
from modules.app_module.domain.entity import Module


class AppModuleRepositoryAdapter(AppModuleRepository):
	def __init__(self, module_repository: AppModuleRepository):
		self.module_repository = module_repository

	async def get_modules_by_ids(
		self, ids: list[int]
	) -> List[Module] | Sequence[Module]:
		return await self.module_repository.get_modules_by_ids(ids)

	async def get_module_list(
		self, limit: int, page: int
	) -> List[Module] | Sequence[Module]:
		return await self.module_repository.get_module_list(limit, page)

	async def get_modules_by_token_name(
		self, token_name_list: list[str]
	) -> List[Module] | Sequence[Module]:
		return await self.module_repository.get_modules_by_token_name(token_name_list)
