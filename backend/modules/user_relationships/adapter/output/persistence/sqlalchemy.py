from typing import Any, Sequence, Type
from uuid import UUID

from sqlalchemy.orm import DeclarativeMeta
from modules.user_relationships.domain.entity import UserRelationshipLink
from modules.user_relationships.domain.repository import UserRelationshipRepository
from modules.user_relationships.adapter.output.persistence.exception import (
	OutputPortException,
)
from core.db import session_factory, Transactional, session

from sqlmodel import delete, col, select, SQLModel


class UserRelationshipSQLAlchemyRepository(UserRelationshipRepository):
	@Transactional()
	async def link_user_entity(self, fk_user: UUID, fk_entity: int, entity_type: str):
		link = UserRelationshipLink(
			fk_user=fk_user,
			fk_entity=fk_entity,
			entity_name=entity_type,
		)
		session.add(link)
		await session.commit()

	@Transactional()
	async def unlink_user_entity(
		self, fk_user: UUID, fk_entity: int, entity_type: str
	) -> bool:
		stmt = (
			delete(UserRelationshipLink)
			.where(col(UserRelationshipLink.fk_user) == fk_user)
			.where(col(UserRelationshipLink.fk_entity) == fk_entity)
			.where(col(UserRelationshipLink.entity_name) == entity_type)
		)

		result = await session.execute(stmt)
		return bool(result.rowcount)

	async def get_by_user_and_entity(
		self, user_id: UUID, entity_name: str, entity: type
	) -> list[Any] | Sequence[SQLModel]:
		stmt = (
			select(entity)
			.join(UserRelationshipLink, UserRelationshipLink.fk_entity == entity.id)
			.where(
				(UserRelationshipLink.fk_user == user_id)
				& (UserRelationshipLink.entity_name == entity_name)
			)
		)
		result = await session.execute(stmt)
		return result.scalars().all()

	async def get_entity_instance_by_id(
		self, id: int, entity: type
	) -> Type[Any] | None:
		if not isinstance(entity, DeclarativeMeta):
			raise OutputPortException

		async with session_factory() as session:
			entity_record = await session.get(entity, int(id))

		return entity_record
