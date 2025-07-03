
from abc import ABC, abstractmethod
from typing import List
from app.module.domain.entity import Module


class ModuleRepository(ABC):


	@abstractmethod
	async def get_modules_by_ids(self, ids: list[int]) -> List[Module]: ...
