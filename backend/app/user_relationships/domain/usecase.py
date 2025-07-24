from dataclasses import dataclass
from typing import Any
import uuid
from app.user_relationships.domain.ports import EntityResolver

from app.user_relationships.domain.repository import UserRelationshipRepository
from app.user_relationships.adapter.output.persistence.exception import EntityInstanceNotFoundException


@dataclass
class GetUserEntitiesUseCase:
	resolver: EntityResolver
	user_relationship_repository: UserRelationshipRepository

	async def __call__(self, user_id: uuid.UUID, entity_type: str):
		entity = self.resolver.resolve(entity_type)
		return await self.user_relationship_repository.get_by_user_and_entity(
			user_id, entity_type, entity
		)


@dataclass
class GetEntityInstanceByIdUseCase:
	resolver: EntityResolver
	user_relationship_repository: UserRelationshipRepository

	async def __call__(self, entity_id : int, entity_type : str) -> type[Any]:
		entity = self.resolver.resolve(entity_type)
		record =  await self.user_relationship_repository.get_entity_by_id(entity_id,entity)
		if not record:
			raise EntityInstanceNotFoundException
		return record


@dataclass
class AssociateUserWithEntityUseCase:
	resolver: EntityResolver
	user_relationship_repository: UserRelationshipRepository

	async def __call__(self, user_uuid : uuid.UUID, id_entity : int, entity_type : str) -> type[Any]:
		entity = self.resolver.resolve(entity_type)
		record =  await self.user_relationship_repository.get_entity_by_id(id_entity,entity)
		if not record:
			raise EntityInstanceNotFoundException
		return record

@dataclass
class UserRelationshipUseCaseFactory:
	resolver: EntityResolver
	user_relationship_repository: UserRelationshipRepository

	def __post_init__(self):
		self.get_user_entities = GetUserEntitiesUseCase(
			self.resolver, self.user_relationship_repository
		)
		self.get_entity_instance_by_id = GetEntityInstanceByIdUseCase(
			self.resolver, self.user_relationship_repository
		)
		self.associate_user_with_entity = AssociateUserWithEntityUseCase(
			self.resolver, self.user_relationship_repository
		)
