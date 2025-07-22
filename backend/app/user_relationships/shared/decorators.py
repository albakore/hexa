from typing import Type
from sqlmodel import SQLModel
from app.user_relationships.infra.output.registry import EntityRelationshipRegistry

def user_relationship(entity_name: str):
    def wrapper(cls: Type[SQLModel]):
        EntityRelationshipRegistry.register(entity_name, cls)
        return cls
    return wrapper