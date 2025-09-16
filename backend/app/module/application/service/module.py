from typing import List, Sequence
from app.module.domain.entity.module import Module
from app.module.domain.repository.module import AppModuleRepository
from app.module.domain.usecase.module import ModuleUseCaseFactory


class AppModuleService:
	def __init__(self, app_module_repository: AppModuleRepository):
		self.repository = app_module_repository
		self.usecase = ModuleUseCaseFactory(app_module_repository)

	async def get_module_list(
		self, limit: int, page: int
	) -> List[Module] | Sequence[Module]:
		return await self.usecase.get_module_list(limit, page)

	async def get_modules_by_ids(
		self, module_ids: list[int]
	) -> List[Module] | Sequence[Module]:
		return await self.usecase.get_module_by_ids(module_ids)
