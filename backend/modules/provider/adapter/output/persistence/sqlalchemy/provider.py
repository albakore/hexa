from typing import Sequence
from sqlmodel import or_, select
from sqlalchemy.orm import selectinload

from modules.provider.domain.entity.provider import Provider
from modules.provider.domain.repository.provider import ProviderRepository

from core.db.session import session as global_session, session_factory


class ProviderSQLAlchemyRepository(ProviderRepository):
	async def get_all_providers(
		self, limit: int = 12, page: int = 0
	) -> list[Provider] | Sequence[Provider]:
		query = select(Provider)
		query = query.slice(page, limit)

		async with session_factory() as session:
			result = await session.execute(query)

		return result.scalars().all()

	async def get_provider_by_id(self, id_provider: int) -> Provider | None:
		stmt = select(Provider).where(Provider.id == int(id_provider))

		async with session_factory() as session:
			instance = await session.execute(stmt)
		return instance.scalars().one_or_none()

	async def save(self, provider: Provider) -> Provider | None:
		global_session.add(provider)
		await global_session.flush()
		return provider

	async def delete(self, provider: Provider):
		await global_session.delete(provider)
		await global_session.flush()
