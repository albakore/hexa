from fastapi import APIRouter, Query, Depends
from shared.dependencies import get_app_module_service

module_router = APIRouter()


@module_router.get("")
async def get_app_module_list(
	limit: int = Query(default=10, ge=1, le=50),
	page: int = Query(default=0),
	module_service = Depends(get_app_module_service),
):
	return await module_service.get_module_list(int(limit), int(page))
