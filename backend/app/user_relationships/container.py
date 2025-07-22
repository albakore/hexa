from dependency_injector.providers import Container, Factory, Singleton
from dependency_injector.containers import DeclarativeContainer, WiringConfiguration

from app.user_relationships.application.service import UserRelationshipService
from app.user_relationships.infra.output.persistence.sqlalchemy import UserRelationshipSQLAlchemyRepository
from app.user_relationships.infra.output.registry import EntityRelationshipRegistry

class UserRelationshipContainer(DeclarativeContainer):
	resolver = Singleton(EntityRelationshipRegistry)
	user_relationship_repository = Factory(UserRelationshipSQLAlchemyRepository)
	service = Factory(
		UserRelationshipService,
		resolver=resolver,
		user_relationship_repository=user_relationship_repository
	)