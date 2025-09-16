from typing import List, Sequence
from app.module.domain.repository.module import AppModuleRepository
from app.module.domain.entity import Module


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
