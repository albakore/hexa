from typing import Protocol

from sqlmodel import SQLModel


class EntityResolver(Protocol):
	def resolve(self, entity_name: str) -> type[SQLModel]: ...
