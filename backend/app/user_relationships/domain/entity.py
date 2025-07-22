
import uuid

from sqlmodel import Field, SQLModel

class UserRelationshipLink(SQLModel, table=True):
    fk_user: uuid.UUID = Field(foreign_key="user.id", primary_key=True)
    fk_entity: int = Field(primary_key=True)
    entity_name: str = Field(primary_key=True)