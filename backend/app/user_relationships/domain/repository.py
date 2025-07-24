from abc import ABC, abstractmethod
from typing import Any, Type
import uuid


class UserRelationshipRepository(ABC):
	@abstractmethod
	async def link_user_entity(
		self, fk_user: uuid.UUID, fk_entity: int, entity_type: str
	): ...

	@abstractmethod
	async def unlink_user_entity(
		self, fk_user: uuid.UUID, fk_entity: int, entity_type: str
	): ...

	@abstractmethod
	async def get_by_user_and_entity(
		self, user_id: uuid.UUID, entity_name: str, entity: type
	) -> list[Any]: ...

	@abstractmethod
	async def get_entity_by_id(
		self, id: int, entity: type
	) -> Type[Any] | None: ...
