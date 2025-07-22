from typing import Type
from sqlmodel import SQLModel
from app.user_relationships.infra.output.registry import EntityRelationshipRegistry

def entity_related(name: str):
    def wrapper(cls: Type[SQLModel]):
        EntityRelationshipRegistry.register(name, cls)
        return cls
    return wrapper