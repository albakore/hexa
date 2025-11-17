import uuid
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Header

from modules.user_relationships.application.service import UserRelationshipService
from modules.user_relationships.container import UserRelationshipContainer

user_relationship_router = APIRouter()


@user_relationship_router.get("/entity")
@inject
async def get_entity_instance(
	entity_key: str,
	entity_id: int,
	service: UserRelationshipService = Depends(
		Provide[UserRelationshipContainer.service]
	),
):
	return await service.get_entity_instance(entity_id, entity_key)


@user_relationship_router.get("/{user_uuid}")
@inject
async def get_relationship(
	user_uuid: uuid.UUID,
	entity_key: str = Header(...),
	service: UserRelationshipService = Depends(
		Provide[UserRelationshipContainer.service]
	),
):
	return await service.get_entities(user_uuid, entity_key)


@user_relationship_router.post("/{user_uuid}/link")
@inject
async def associate_user_with_entity(
	user_uuid: uuid.UUID,
	entity_key: str = Header(...),
	entity_id: int = Header(...),
	service: UserRelationshipService = Depends(
		Provide[UserRelationshipContainer.service]
	),
):
	return await service.associate_user_with_entity(user_uuid, entity_id, entity_key)


@user_relationship_router.delete("/{user_uuid}/link")
@inject
async def delete_association_user_with_entity(
	user_uuid: uuid.UUID,
	entity_key: str = Header(...),
	entity_id: int = Header(...),
	service: UserRelationshipService = Depends(
		Provide[UserRelationshipContainer.service]
	),
):
	return await service.delete_association_user_with_entity(
		user_uuid, entity_id, entity_key
	)
