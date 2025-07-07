
from typing import List, Sequence

from sqlmodel import col, select
from app.module.domain.entity import Module
from app.module.domain.repository.module import AppModuleRepository
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

