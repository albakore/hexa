from typing import Dict, Type
from sqlmodel import SQLModel

from app.user_relationships.domain.ports import EntityResolver
from app.user_relationships.domain.exception import EntityRelationShipNotFoundException


class EntityRelationshipRegistry(EntityResolver):
    _registry: dict[str, Type[SQLModel]] = {}

    def resolve(self, tipo: str) -> type:
        try:
            return self._registry[tipo]
        except KeyError:
            raise EntityRelationShipNotFoundException

    @classmethod
    def register(cls, tipo: str, model: type):
        cls._registry[tipo] = model