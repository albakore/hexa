from ast import List
from typing import Any, Sequence
from uuid import UUID
from app.user_relationships.domain.entity import UserRelationshipLink
from app.user_relationships.domain.repository import UserRelationshipRepository
from core.db import session_factory, Transactional, session

from sqlmodel import delete, col, select, SQLModel
from pydantic import BaseModel


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
	async def unlink_user_entity(self, fk_user: UUID, fk_entity: int, entity_type: str):
		stmt = delete(UserRelationshipLink)\
			.where(col(UserRelationshipLink.fk_user) == fk_user)\
			.where(col(UserRelationshipLink.fk_entity) == fk_entity)\
			.where(col(UserRelationshipLink.entity_name) == entity_type)

		await session.execute(stmt)

	async def get_by_user_and_entity(
		self, user_id: UUID, entity_name: str, entity: type
	) -> list[Any] | Sequence[SQLModel]:
		stmt = (
			select(entity)
			.join(
				UserRelationshipLink,
				UserRelationshipLink.fk_entity == entity.id
			)
			.where(
				(UserRelationshipLink.fk_user == user_id)
				& (UserRelationshipLink.entity_name == entity_name)
			)
		)
		result = await session.execute(stmt)
		return result.scalars().all()
