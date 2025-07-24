import uuid
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Form, Header, Query, Response

from app.user_relationships.application.service import UserRelationshipService
from app.user_relationships.container import UserRelationshipContainer
from app.container import SystemContainer

user_relationship_router = APIRouter()


@user_relationship_router.get("/entity")
@inject
async def get_entity_instance(
	entity_key: str,
	entity_id: int,
	service : UserRelationshipService = Depends(Provide[SystemContainer.user_relationship.service])
):
	return await service.get_entity_instance(entity_id, entity_key)

@user_relationship_router.get("/{user_uuid}")
@inject
async def get_relationship(
	user_uuid: uuid.UUID,
	entity_key: str = Header(...),
	service : UserRelationshipService = Depends(Provide[SystemContainer.user_relationship.service])
):
	return await service.get_entities(user_uuid, entity_key)