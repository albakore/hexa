from typing import List, Sequence
from sqlmodel import select

from core.db.session import session as global_session, session_factory
from core.search import DynamicSearchMixin
from modules.provider.domain.entity.provider import Provider
from modules.provider.domain.repository.provider import ProviderRepository
from modules.provider.domain.command import SearchProviderCommand


class ProviderSQLAlchemyRepository(DynamicSearchMixin, ProviderRepository):
	model_class = Provider
	date_fields = set()  # Provider no tiene campos de fecha

	async def get_all_providers(
		self, limit: int = 12, page: int = 0
	) -> list[Provider] | Sequence[Provider]:
		query = select(Provider)
		offset = page * limit
		query = query.offset(offset).limit(limit)

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

	async def search_providers(
		self, command: SearchProviderCommand
	) -> tuple[List[Provider] | Sequence[Provider], int]:
		"""Búsqueda dinámica de proveedores con filtros"""
		async with session_factory() as session:
			return await self.dynamic_search(
				session=session,
				filters=command.filters,
				limit=command.limit,
				page=command.page
			)
