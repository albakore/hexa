from typing import List, Sequence
from modules.app_module.domain.entity.module import Module
from modules.app_module.domain.repository.module import AppModuleRepository
from modules.app_module.domain.usecase.module import ModuleUseCaseFactory


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

	async def get_modules_by_token_name(
		self, token_name_list: list[str]
	) -> List[Module] | Sequence[Module]:
		return await self.usecase.get_modules_by_token_name(token_name_list)
