from abc import ABC, abstractmethod
from typing import List, Sequence
from modules.module.domain.entity import Module


class AppModuleRepository(ABC):
	@abstractmethod
	async def get_module_list(
		self, limit: int, page: int
	) -> List[Module] | Sequence[Module]: ...

	@abstractmethod
	async def get_modules_by_ids(
		self, ids: list[int]
	) -> List[Module] | Sequence[Module]: ...

	@abstractmethod
	async def get_modules_by_token_name(
		self, token_name_list: list[str]
	) -> List[Module] | Sequence[Module]: ...
