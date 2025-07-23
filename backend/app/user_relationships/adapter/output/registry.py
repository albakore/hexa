from typing import Dict, Type
from sqlmodel import SQLModel

from app.user_relationships.domain.ports import EntityResolver


class EntityRelationshipRegistry(EntityResolver):
    _registry: dict[str, Type[SQLModel]] = {}

    def resolve(self, tipo: str) -> type:
        return self._registry[tipo]

    @classmethod
    def register(cls, tipo: str, model: type):
        cls._registry[tipo] = model