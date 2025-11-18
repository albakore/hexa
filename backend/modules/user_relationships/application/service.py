from dataclasses import dataclass
import uuid

from modules.user_relationships.domain.ports import EntityResolver
from modules.user_relationships.domain.repository import UserRelationshipRepository
from modules.user_relationships.application.usecase import UserRelationshipUseCaseFactory


@dataclass
class UserRelationshipService:
	resolver: EntityResolver
	user_relationship_repository: UserRelationshipRepository

	def __post_init__(self):
		self.usecase = UserRelationshipUseCaseFactory(
			self.resolver, self.user_relationship_repository
		)

	async def get_entities(self, user_uuid: uuid.UUID, entity_type: str):
		entities = await self.usecase.get_user_entities(user_uuid, entity_type)
		return entities

	async def get_entity_instance(self, entity_id: int, entity_type: str):
		entities = await self.usecase.get_entity_instance_by_id(entity_id, entity_type)
		return entities

	async def associate_user_with_entity(
		self, user_uuid: uuid.UUID, id_entity: int, entity_type: str
	):
		await self.usecase.associate_user_with_entity(user_uuid, id_entity, entity_type)
		return True

	async def delete_association_user_with_entity(
		self, user_uuid: uuid.UUID, id_entity: int, entity_type: str
	):
		return await self.usecase.delete_association_user_with_entity(
			user_uuid, id_entity, entity_type
		)
