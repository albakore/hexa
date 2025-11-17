from dataclasses import dataclass
from typing import Any
import uuid
from modules.user_relationships.domain.ports import EntityResolver

from modules.user_relationships.domain.repository import UserRelationshipRepository
from modules.user_relationships.adapter.output.persistence.exception import (
	EntityInstanceNotFoundException,
)
from modules.user_relationships.domain.exception import (
	DuplicateAssociationException,
	EntityInstanceNotDeletedException,
)


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

	async def __call__(self, entity_id: int, entity_type: str) -> type[Any]:
		entity = self.resolver.resolve(entity_type)
		entity_instance = (
			await self.user_relationship_repository.get_entity_instance_by_id(
				entity_id, entity
			)
		)
		if not entity_instance:
			raise EntityInstanceNotFoundException
		return entity_instance


@dataclass
class AssociateUserWithEntityUseCase:
	resolver: EntityResolver
	user_relationship_repository: UserRelationshipRepository

	async def __call__(
		self, user_uuid: uuid.UUID, id_entity: int, entity_type: str
	) -> None:
		entity = self.resolver.resolve(entity_type)
		entity_instance = (
			await self.user_relationship_repository.get_entity_instance_by_id(
				id_entity, entity
			)
		)
		if not entity_instance:
			raise EntityInstanceNotFoundException
		try:
			await self.user_relationship_repository.link_user_entity(
				user_uuid, id_entity, entity_type
			)
		except Exception:
			raise DuplicateAssociationException


@dataclass
class DeleteAssociationUserWithEntityUseCase:
	resolver: EntityResolver
	user_relationship_repository: UserRelationshipRepository

	async def __call__(self, user_uuid: uuid.UUID, id_entity: int, entity_type: str):
		self.resolver.resolve(entity_type)
		is_deleted = await self.user_relationship_repository.unlink_user_entity(
			user_uuid, id_entity, entity_type
		)
		if not is_deleted:
			raise EntityInstanceNotDeletedException
		return is_deleted


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
		self.delete_association_user_with_entity = (
			DeleteAssociationUserWithEntityUseCase(
				self.resolver, self.user_relationship_repository
			)
		)
