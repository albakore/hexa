from typing import List, Sequence

from sqlmodel import col, select
from modules.module.domain.entity import Module
from modules.module.domain.repository.module import AppModuleRepository
from core.db.session import session_factory


class AppModuleSQLAlchemyRepository(AppModuleRepository):
	async def get_modules_by_ids(
		self, ids: list[int]
	) -> List[Module] | Sequence[Module]:
		if not ids:
			return []
		stmt = select(Module).where(col(Module.id).in_(ids))
		async with session_factory() as session:
			result = await session.execute(stmt)
		return result.scalars().all()

	async def get_module_list(
		self, limit: int, page: int
	) -> List[Module] | Sequence[Module]:
		query = select(Module)
		query = query.slice(page, limit)

		async with session_factory() as session:
			result = await session.execute(query)

		return result.scalars().all()

	async def get_modules_by_token_name(
		self, token_name_list: list[str]
	) -> List[Module] | Sequence[Module]:
		query = select(Module).where(col(Module.token).in_(token_name_list))

		async with session_factory() as session:
			result = await session.execute(query)

		return result.scalars().all()
