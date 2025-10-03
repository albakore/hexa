from fastapi import APIRouter

from modules.file_storage.adapter.input.api.v1.file_storage import (
	file_storage_router as file_storage_v1_router,
)

router = APIRouter()
router.include_router(
	file_storage_v1_router,
	prefix="/filestorage/v1/filestorage",
	tags=["File Storage Service"],
)
__all__ = ["router"]
