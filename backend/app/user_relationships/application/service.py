from dataclasses import dataclass
import uuid
from sqlmodel import Session, select
from typing import List
from uuid import UUID

from app.user_relationships.domain.ports import EntityResolver
from app.user_relationships.domain.repository import UserRelationshipRepository
from app.user_relationships.domain.usecase import UserRelationshipUseCaseFactory

@dataclass
class UserRelationshipService:
    resolver : EntityResolver
    user_relationship_repository : UserRelationshipRepository

    def __post_init__(self):
        self.usecase = UserRelationshipUseCaseFactory(
            self.resolver,
            self.user_relationship_repository
        )

    async def get_entities(self, user_uuid : uuid.UUID, entity_type : str):
        entities = await self.usecase.get_user_entities(
            user_uuid,
            entity_type
        )
        return entities