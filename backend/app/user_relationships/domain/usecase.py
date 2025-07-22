from dataclasses import dataclass
import uuid
from app.user_relationships.domain.ports import EntityResolver

from app.user_relationships.domain.repository import UserRelationshipRepository


@dataclass
class GetUserEntitiesUseCase:
	resolver: EntityResolver
	user_relationship_repository: UserRelationshipRepository

	async def __call__(self, user_id: uuid.UUID, entity_type: str):
		entity = self.resolver.resolve(entity_type)
		return await self.user_relationship_repository.get_by_user_and_entity(user_id, entity_type, entity)


@dataclass
class UserRelationshipUseCaseFactory:
	resolver: EntityResolver
	user_relationship_repository: UserRelationshipRepository

	def __post_init__(self):
		self.get_user_entities = GetUserEntitiesUseCase(
			self.resolver,
			self.user_relationship_repository
		)