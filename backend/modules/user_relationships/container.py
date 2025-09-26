from dependency_injector.providers import Container, Factory, Singleton
from dependency_injector.containers import DeclarativeContainer, WiringConfiguration

from modules.user_relationships.application.service import UserRelationshipService
from modules.user_relationships.adapter.output.persistence.sqlalchemy import (
	UserRelationshipSQLAlchemyRepository,
)
from modules.user_relationships.adapter.output.registry import (
	EntityRelationshipRegistry,
)


class UserRelationshipContainer(DeclarativeContainer):
	wiring_config = WiringConfiguration(
		packages=["modules.user_relationships"], auto_wire=True
	)

	resolver = Singleton(EntityRelationshipRegistry)
	user_relationship_repository = Factory(UserRelationshipSQLAlchemyRepository)
	service = Factory(
		UserRelationshipService,
		resolver=resolver,
		user_relationship_repository=user_relationship_repository,
	)
