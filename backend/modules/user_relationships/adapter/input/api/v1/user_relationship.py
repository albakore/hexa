import uuid
from fastapi import APIRouter, Depends
from shared.dependencies import get_user_relationship_service

user_relationship_router = APIRouter()


@user_relationship_router.get("/entity")
async def get_entity_instance(
	entity_key: str,
	entity_id: int,
	service = Depends(get_user_relationship_service),
):
	return await service.get_entity_instance(entity_id, entity_key)


@user_relationship_router.get("/{user_uuid}")
async def get_relationship(
	user_uuid: uuid.UUID,
	entity_key: str,
	service = Depends(get_user_relationship_service),
):
	return await service.get_entities(user_uuid, entity_key)


@user_relationship_router.post("/{user_uuid}/link")
async def associate_user_with_entity(
	user_uuid: uuid.UUID,
	entity_key: str,
	entity_id: int,
	service = Depends(get_user_relationship_service),
):
	return await service.associate_user_with_entity(user_uuid, entity_id, entity_key)


@user_relationship_router.delete("/{user_uuid}/link")
async def delete_association_user_with_entity(
	user_uuid: uuid.UUID,
	entity_key: str,
	entity_id: int,
	service = Depends(get_user_relationship_service),
):
	return await service.delete_association_user_with_entity(
		user_uuid, entity_id, entity_key
	)
